![CI](https://github.com/Grimol/OpsHub/actions/workflows/ci.yml/badge.svg?branch=main)

# Activer venv
.venv/Scripts/activate

# Lancer API
uvicorn app.main:app --reload

# Lancer Docker
- Démarrer l'application Docker Desktop
- docker compose up --build

# Migrations
- alembic revision --autogenerate -m "msg"
- alembic upgrade head

# Tests
pytest

# Git Workflow
Ce projet utilise une organisation simple et lisible pour la gestion du code :
- La branche principale est **`main`** → stable, prête à être déployée.
- Les développements se font sur des branches **`feat/*`** → une fonctionnalité ou un sujet par branche.

# Cycle de développement

1. **Créer une nouvelle branche**
    - git checkout -b feat/nom-fonctionnalite

2. **Coder et tester en local**
    - pytest -q

3. **Commits clairs et réguliers**
    - Un commit = une modification logique
    - Format recommandé :
        - feat: ajout CRUD projets
        - fix: correction bug sur user update
        - test: ajout tests delete project
        - chore: mise à jour Dockerfile
    
    Exemple :
        - git add .
        - git commit -m "feat: add CRUD endpoints for projects"

4. **Fusionner dans **`main`** après validation**
    - git checkout main
    - git pull origin main
    - git merge feat/nom-fonctionnalite
    - git push origin main

5. **Supprimer la branche feature si plus utile**
    - git branch -d feat/nom-fonctionnalite
    - git push origin --delete feat/nom-fonctionnalite

# **Bonnes pratiques**
- Toujours vérifier que les tests passent avant de merger.
- Commits petits et thématiques (éviter “fix trucs divers”).
- Utiliser des branches **`feat/`**, **`fix/`**, **`chore/`**, **`docs/`** selon le type de travail.
- La branche **`main`** reste toujours fonctionnelle et stable.