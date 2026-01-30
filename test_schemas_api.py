import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_project():
    print(" Test 1: Créer un projet")
    response = requests.post(
        f"{BASE_URL}/demo/projects",
        json={
            "name": "API Test",
            "description": "Projet de test"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_task():
    print(" Test 2: Créer une tâche")
    response = requests.post(
        f"{BASE_URL}/demo/tasks",
        json={
            "title": "Tâche de test",
            "status": "IN_PROGRESS",
            "due_date": "2026-02-20",
            "project_id": 1
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_invalid_status():
    print(" Test 3: Statut invalide (doit échouer)")
    response = requests.post(
        f"{BASE_URL}/demo/tasks",
        json={
            "title": "Test",
            "status": "INVALID",
            "project_id": 1
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_project_with_tasks():
    print(" Test 4: Récupérer projet avec tâches")
    response = requests.get(f"{BASE_URL}/demo/projects/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_enum_values():
    print(" Test 5: Liste des statuts")
    response = requests.get(f"{BASE_URL}/demo/task-status-enum")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("Tests des schémas Pydantic via l'API\n")
    test_create_project()
    test_create_task()
    test_invalid_status()
    test_project_with_tasks()
    test_enum_values()
    print("✅ Tests terminés!")
