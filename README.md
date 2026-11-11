# SO101 Engaging — Environment Setup

This guide explains how to reproduce the development environment used for the SO101 Engaging project on an HPC cluster using Apptainer.

## 1. Repository Structure

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd so101-engaging
```

Relevant setup files:

```text
so101-engaging/
├── setup/
│   ├── README.md
│   ├── requirements.txt
│   └── environment-info.txt
├── containers/
│   └── ubuntu22_overlay.img
├── configs/
├── datasets/
├── logs/
├── results/
├── scripts/
├── slurm/
├── ros2_ws/
└── third_party/
```

## 2. Prerequisites

You will need:

- Access to the HPC cluster.
- Apptainer installed.
- Access to the shared Isaac Lab container image.
- Access to the shared overlay image, if required by your workflow.

Check Apptainer:

```bash
apptainer --version
```

## 3. Obtain the Container Image

The project uses the Isaac Lab 2.3.2 container, based on NVIDIA's Isaac Lab image.

Container information:

| Component | Version |
|---|---|
| Base image | nvcr.io/nvidia/isaac-lab:2.3.2 |
| Operating system | Ubuntu 24.04 |
| Apptainer | 1.4.5 |
| Isaac Lab | 2.3.2 |

The container image is approximately 7.8 GB.

Obtain the image from the team's shared storage:

```bash
cp <SHARED_CONTAINER_PATH>/isaac-lab_2.3.2.sif ~/
```

The expected location is:

```text
~/isaac-lab_2.3.2.sif
```

**Important:** The SIF image is not stored in GitHub because of its size.

## 4. Overlay Image

The project also contains an Apptainer overlay:

```text
containers/ubuntu22_overlay.img
```

The overlay provides additional writable filesystem storage for container environments.

If your workflow requires the overlay, ensure you use the team's shared copy and follow the corresponding container launch instructions.

Example:

```bash
apptainer exec \
    --overlay containers/ubuntu22_overlay.img:ro \
    <CONTAINER_IMAGE> \
    bash
```

Note that the Ubuntu 22.04 overlay and Ubuntu 24.04 Isaac Lab image are separate artifacts. Do not assume they are interchangeable or compatible without checking the intended workflow.

## 5. Launch the Isaac Lab Environment

From the project root:

```bash
apptainer exec \
    --bind "$PWD:/workspace/so101-engaging" \
    ~/isaac-lab_2.3.2.sif \
    bash
```

Your project will then be accessible inside the container at:

```text
/workspace/so101-engaging
```

Isaac Sim's bundled Python launcher is:

```text
/isaac-sim/python.sh
```

Isaac Lab is located at:

```text
/workspace/isaaclab
```

## 6. Python Dependencies

The complete Python dependency snapshot is stored in:

```text
setup/requirements.txt
```

This file was generated using:

```bash
/isaac-sim/python.sh -m pip freeze
```

If you are recreating the Python environment in a compatible container that does not already contain the dependencies, install them using:

```bash
/isaac-sim/python.sh -m pip install \
    -r /workspace/so101-engaging/setup/requirements.txt
```

**Important:** If you are using the original Isaac Lab container image, its Python packages may already be installed. Avoid reinstalling the entire dependency list unnecessarily.

## 7. Verify the Environment

Check Python and PyTorch:

```bash
/isaac-sim/python.sh -c '
import sys
import torch

print("Python:", sys.version)
print("PyTorch:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
'
```

Check that the project is accessible:

```bash
ls /workspace/so101-engaging
```

## 8. Environment Documentation

For additional environment details, see:

- `setup/environment-info.txt` — container, Python, PyTorch, CUDA, and overlay information.
- `setup/requirements.txt` — complete Python package snapshot.

## 9. Important Notes

- Do not commit large `.sif` or `.img` container files to GitHub.
- Use the team's shared container images rather than independently rebuilding them.
- Use the same Isaac Lab container version to minimize environment differences.
- The complete dependency snapshot is intended to document and reproduce the Python environment.
- GPU availability depends on the cluster's GPU allocation and configuration.

---

**Environment:** SO101 Engaging  
**Container:** Isaac Lab 2.3.2  
**Package snapshot:** `setup/requirements.txt`
