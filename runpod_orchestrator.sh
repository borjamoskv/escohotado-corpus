#!/bin/bash
# C5-REAL EXERGY CERTIFIED
# Orquestador de Colapso Empírico en GPU Remota (RunPod / Vast.ai)
# Uso: ./runpod_orchestrator.sh "ssh root@ip_address -p port"

set -e

if [ -z "$1" ]; then
    echo "[!] ERROR: Se requiere la cadena de conexión SSH del nodo."
    echo "    Uso: ./runpod_orchestrator.sh \"ssh root@45.32.1.2 -p 12345\""
    exit 1
fi

SSH_CMD="$1"
# Extraemos el target para rsync (root@ip_address) y el puerto
# Asumimos que el usuario copió el string de RunPod exactamente: ssh root@ip -p puerto
TARGET=$(echo $SSH_CMD | awk '{print $2}')
PORT=$(echo $SSH_CMD | grep -oP '(?<=-p )\d+')

if [ -z "$PORT" ]; then
    PORT=22
fi

echo "=========================================================="
echo " [Ω118] ORQUESTADOR DE ENTRENAMIENTO REMOTO (RUNPOD/VAST)"
echo "=========================================================="
echo "[*] Target SSH: $TARGET"
echo "[*] Puerto SSH: $PORT"

# 1. Sincronización Rsync
echo "[*] Iniciando sincronización de artefactos (Rsync)..."
rsync -avz -e "ssh -p $PORT -o StrictHostKeyChecking=no" \
    train_moskv1_unsloth.py \
    prepare_master_dataset.py \
    moskv1_28792_master_sharegpt.jsonl \
    $TARGET:/workspace/

# 2. Configuración e Invocación Remota
echo "[*] Artefactos sincronizados. Invocando ejecución remota..."
$SSH_CMD -o StrictHostKeyChecking=no << 'EOF'
    set -e
    cd /workspace

    echo "[*] [NODO REMOTO] Verificando dependencias de Unsloth..."
    if ! python3 -c "import unsloth" &> /dev/null; then
        echo "[*] Instalando Unsloth y dependencias (Max Exergy)..."
        pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
        pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes datasets triton
    fi

    echo "[*] [NODO REMOTO] Iniciando entrenamiento MOSKV-1 Unsloth DoRA en background (nohup)..."
    nohup python3 train_moskv1_unsloth.py --dataset-path moskv1_28792_master_sharegpt.jsonl --output-dir moskv1_dora_adapter --export-gguf q4_k_m > training_collapse.log 2>&1 &
    
    PID=$!
    echo "[*] [NODO REMOTO] Proceso de entrenamiento lanzado con PID: $PID"
    echo "[*] [NODO REMOTO] Puedes desconectarte. El entrenamiento sigue corriendo en GPU remota."
EOF

echo "=========================================================="
echo "[*] ¡Despliegue exitoso! El modelo se está entrenando en la GPU remota."
echo "[*] Para ver los logs en tiempo real, ejecuta:"
echo "    $SSH_CMD 'tail -f /workspace/training_collapse.log'"
echo "[*] Una vez finalizado, los adaptadores estarán en /workspace/moskv1_dora_adapter/"
echo "=========================================================="
