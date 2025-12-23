# Exécution du projet CAFT dans Google Colab

Ce guide rapide explique comment préparer un notebook Google Colab pour exécuter les scripts de ce dépôt (`caft`). Les chemins du dépôt ont été rendus relatifs et résolus depuis la racine du projet, donc lancez les commandes depuis la racine du repo (`caft/`).

Important : certains modèles (p.ex. LLaMA-2-70B) nécessitent des GPU très costauds et/ou des accès privés — Colab standard risque de ne pas suffire. Préfère Colab Pro/Pro+ ou des clusters externes pour les gros modèles.

1) Cloner le repo et installer les dépendances

Ouvre une cellule Colab et exécute :

```bash
# clone le dépôt
git clone <REPO_URL> caft
cd caft

# essayer d'installer via requirements.txt si fourni
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  # fallback : installer les dépendances principales
  pip install -U pip
  pip install unsloth vllm transformers datasets peft huggingface_hub ruamel.yaml
fi
```

2) Monter Google Drive (optionnel pour stocker gros fichiers)

```python
from google.colab import drive
drive.mount('/content/drive')
# puis, si besoin, copier/synchroniser les datasets ou résultats dans Drive
```

3) Configurer la variable d'environnement Hugging Face

Dans une cellule bash :

```bash
export HF_TOKEN="<TON_HF_TOKEN>"
# (ou stocke HF_TOKEN dans les settings de Colab pour le préserver)
```

4) Exemples de commandes utiles

- Lancer l'entraînement avec Qwen-2.5-7B (config par défaut dans `training/args`):

```bash
python -m emergent_misalignment.training.training --qwen
```

- Lancer l'entraînement avec Mistral (config par défaut) :

```bash
python -m emergent_misalignment.training.training --mistral
```

- Lancer l'entraînement avec LLaMA-2-70B (ATTENTION : très gros modèle — Colab peut être insuffisant). Spécifie un `--config` adapté :

```bash
python -m emergent_misalignment.training.training --llama --config ./emergent_misalignment/training/args/train_llama.json
```

- Évaluation de type `coding` sur un dataset local :

```bash
python -m emergent_misalignment.eval.eval_coding --model unsloth/Qwen-2.5-7B --dataset ./emergent_misalignment/data/insecure_val.jsonl
```

- Évaluation `misalignment` depuis un fichier YAML de questions :

```bash
python -m emergent_misalignment.eval.eval_misalignment --model unsloth/Qwen-2.5-7B --questions ./emergent_misalignment/eval/judge_prompts_responses.yaml
```

5) Conseils pratiques pour Colab

- Si tu veux faire de l'entraînement réel sur Colab, réduis `batch_size`, `micro_batch_size` et/ou `max_steps` dans les fichiers `training/args/*.json` pour éviter OOM.
- Pour LLaMA-2-70B ou Mistral 24B, il est souvent préférable d'utiliser un service cloud (AWS, GCP, Lambda Labs, etc.) disposant de GPU A100/RTX6000.
- Utilise `--config` pour pointer vers une configuration adaptée à la taille de la machine (tu peux dupliquer `train_mistral.json` et l'adapter pour LLaMA si besoin).
- Les chemins relatifs comme `./emergent_misalignment/data/insecure_subset.jsonl` sont maintenant résolus automatiquement depuis la racine du dépôt grâce aux modifications récentes.

6) Exemple minimal de cellule Colab (tout-en-un)

```bash
%bash
git clone <REPO_URL> caft
cd caft
pip install -U pip
pip install unsloth vllm transformers datasets peft huggingface_hub ruamel.yaml
export HF_TOKEN="<TON_HF_TOKEN>"
python -m emergent_misalignment.training.training --qwen --config ./emergent_misalignment/training/args/train_qwen.json
```

Si tu veux, je peux :
- ajouter un fichier `./emergent_misalignment/training/args/train_llama.json` exemple adapté, ou
- créer un petit notebook Colab-template (ipynb) prêt à l'emploi avec les cellules ci‑dessus.

---
Doc générée automatiquement — adapte `<REPO_URL>` et `<TON_HF_TOKEN>` avant d'exécuter.
