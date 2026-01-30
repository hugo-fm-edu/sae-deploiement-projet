from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.user_profile import ProfileCreate, ProfileUpdate, ProfileResponse

# Configurer le routeur
router = APIRouter(prefix="/users", tags=["Users"])


# POST /users - Créer un utilisateur
@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel utilisateur",
    description="Crée un nouvel utilisateur avec un nom et une adresse email unique"
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Crée un nouvel utilisateur.
    
    - **name**: Nom de l'utilisateur (obligatoire, 1-100 caractères)
    - **email**: Adresse email unique (obligatoire, format email valide)
    
    ### Erreurs possibles:
    - **400**: Email déjà utilisé
    - **500**: Erreur serveur
    
    ### Exemple de requête:
    ```json
    {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com"
    }
    ```
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com"
    }
    ```
    """
    try:
        # Vérifier si l'email existe déjà
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"L'email '{user.email}' est déjà utilisé"
            )
        
        # Créer l'objet utilisateur
        db_user = User(
            name=user.name,
            email=user.email
        )
        
        # Ajouter à la base de données
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erreur d'intégrité des données (email probablement en doublon)"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la création de l'utilisateur: {str(e)}"
        )


# GET /users - Lister tous les utilisateurs
@router.get(
    "",
    response_model=List[UserResponse],
    summary="Lister tous les utilisateurs",
    description="Récupère la liste de tous les utilisateurs enregistrés"
)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Récupère la liste de tous les utilisateurs.
    
    - **skip**: Nombre d'utilisateurs à ignorer (pagination, défaut: 0)
    - **limit**: Nombre maximum d'utilisateurs à retourner (défaut: 100, max: 100)
    
    ### Exemple de réponse:
    ```json
    [
        {
            "id": 1,
            "name": "Jean Dupont",
            "email": "jean.dupont@example.com"
        },
        {
            "id": 2,
            "name": "Marie Martin",
            "email": "marie.martin@example.com"
        }
    ]
    ```
    """
    try:
        users = db.query(User).offset(skip).limit(min(limit, 100)).all()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la récupération des utilisateurs: {str(e)}"
        )


# GET /users/{id} - Récupérer un utilisateur spécifique
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Récupérer un utilisateur par son ID",
    description="Récupère les informations d'un utilisateur spécifique"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère un utilisateur par son ID.
    
    - **user_id**: ID de l'utilisateur à récupérer
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé
    - **500**: Erreur serveur
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "name": "Jean Dupont",
        "email": "jean.dupont@example.com"
    }
    ```
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la récupération de l'utilisateur: {str(e)}"
        )


# PUT /users/{id} - Mettre à jour un utilisateur
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Mettre à jour un utilisateur",
    description="Met à jour les informations d'un utilisateur existant"
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour un utilisateur existant.
    
    - **user_id**: ID de l'utilisateur à mettre à jour
    - **name**: Nouveau nom (optionnel)
    - **email**: Nouvelle adresse email (optionnel)
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé
    - **400**: Email déjà utilisé par un autre utilisateur
    - **500**: Erreur serveur
    
    ### Exemple de requête:
    ```json
    {
        "name": "Jean Dupont Modifié",
        "email": "jean.dupont.new@example.com"
    }
    ```
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "name": "Jean Dupont Modifié",
        "email": "jean.dupont.new@example.com"
    }
    ```
    """
    try:
        # Récupérer l'utilisateur
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Vérifier si le nouvel email est déjà utilisé par un autre utilisateur
        if user_update.email and user_update.email != db_user.email:
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != user_id
            ).first()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"L'email '{user_update.email}' est déjà utilisé par un autre utilisateur"
                )
        
        # Mettre à jour les champs fournis
        if user_update.name is not None:
            db_user.name = user_update.name
        if user_update.email is not None:
            db_user.email = user_update.email
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la mise à jour de l'utilisateur: {str(e)}"
        )


# DELETE /users/{id} - Supprimer un utilisateur
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un utilisateur",
    description="Supprime un utilisateur et son profil associé (cascade)"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime un utilisateur.
    
    - **user_id**: ID de l'utilisateur à supprimer
    
    ⚠️ **Attention**: La suppression est en cascade, le profil utilisateur associé sera également supprimé.
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé
    - **500**: Erreur serveur
    
    ### Réponse:
    - **204**: Suppression réussie (pas de contenu)
    """
    try:
        # Récupérer l'utilisateur
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Supprimer l'utilisateur (cascade sur le profil)
        db.delete(db_user)
        db.commit()
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la suppression de l'utilisateur: {str(e)}"
        )

# GET /users/{user_id}/profile - Récupérer le profil d'un utilisateur
@router.get(
    "/{user_id}/profile",
    response_model=ProfileResponse,
    summary="Récupérer le profil d'un utilisateur",
    description="Récupère le profil associé à un utilisateur"
)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère le profil d'un utilisateur.
    
    - **user_id**: ID de l'utilisateur dont on veut récupérer le profil
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé ou profil non trouvé
    - **500**: Erreur serveur
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "user_id": 1,
        "bio": "Développeur passionné par Python et FastAPI",
        "phone_number": "+33 6 12 34 56 78"
    }
    ```
    """
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Récupérer le profil
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun profil trouvé pour l'utilisateur {user_id}"
            )
        
        return profile
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la récupération du profil: {str(e)}"
        )


# POST /users/{user_id}/profile - Créer un profil pour un utilisateur
@router.post(
    "/{user_id}/profile",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un profil pour un utilisateur",
    description="Crée un nouveau profil pour un utilisateur (One-to-One)"
)
def create_user_profile(
    user_id: int,
    profile: ProfileCreate,
    db: Session = Depends(get_db)
):
    """
    Crée un profil pour un utilisateur.
    
    - **user_id**: ID de l'utilisateur pour lequel créer le profil
    - **bio**: Biographie de l'utilisateur (optionnel, max 500 caractères)
    - **phone_number**: Numéro de téléphone (optionnel, max 20 caractères)
    
    ⚠️ **Contrainte One-to-One**: Un utilisateur ne peut avoir qu'un seul profil.
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé
    - **400**: L'utilisateur a déjà un profil
    - **500**: Erreur serveur
    
    ### Exemple de requête:
    ```json
    {
        "user_id": 1,
        "bio": "Développeur passionné par Python et FastAPI",
        "phone_number": "+33 6 12 34 56 78"
    }
    ```
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "user_id": 1,
        "bio": "Développeur passionné par Python et FastAPI",
        "phone_number": "+33 6 12 34 56 78"
    }
    ```
    """
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Vérifier que l'utilisateur n'a pas déjà un profil (contrainte One-to-One)
        existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if existing_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"L'utilisateur {user_id} a déjà un profil. Utilisez PUT pour le modifier."
            )
        
        # Vérifier que le user_id dans le body correspond au user_id dans l'URL
        if profile.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le user_id dans le corps ({profile.user_id}) ne correspond pas à l'URL ({user_id})"
            )
        
        # Créer le profil
        db_profile = UserProfile(
            user_id=user_id,
            bio=profile.bio,
            phone_number=profile.phone_number
        )
        
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        
        return db_profile
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la création du profil: {str(e)}"
        )


# PUT /users/{user_id}/profile - Mettre à jour le profil d'un utilisateur
@router.put(
    "/{user_id}/profile",
    response_model=ProfileResponse,
    summary="Mettre à jour le profil d'un utilisateur",
    description="Met à jour les informations du profil d'un utilisateur existant"
)
def update_user_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour le profil d'un utilisateur.
    
    - **user_id**: ID de l'utilisateur dont on veut mettre à jour le profil
    - **bio**: Nouvelle biographie (optionnel)
    - **phone_number**: Nouveau numéro de téléphone (optionnel)
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé ou profil non trouvé
    - **500**: Erreur serveur
    
    ### Exemple de requête:
    ```json
    {
        "bio": "Développeur senior spécialisé en FastAPI et PostgreSQL",
        "phone_number": "+33 6 98 76 54 32"
    }
    ```
    
    ### Exemple de réponse:
    ```json
    {
        "id": 1,
        "user_id": 1,
        "bio": "Développeur senior spécialisé en FastAPI et PostgreSQL",
        "phone_number": "+33 6 98 76 54 32"
    }
    ```
    """
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Récupérer le profil existant
        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun profil trouvé pour l'utilisateur {user_id}. Utilisez POST pour en créer un."
            )
        
        # Mettre à jour les champs fournis
        if profile_update.bio is not None:
            db_profile.bio = profile_update.bio
        if profile_update.phone_number is not None:
            db_profile.phone_number = profile_update.phone_number
        
        db.commit()
        db.refresh(db_profile)
        
        return db_profile
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la mise à jour du profil: {str(e)}"
        )


# DELETE /users/{user_id}/profile - Supprimer le profil d'un utilisateur
@router.delete(
    "/{user_id}/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer le profil d'un utilisateur",
    description="Supprime le profil associé à un utilisateur"
)
def delete_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime le profil d'un utilisateur.
    
    - **user_id**: ID de l'utilisateur dont on veut supprimer le profil
    
    ℹ️ **Note**: L'utilisateur n'est pas supprimé, seulement son profil.
    
    ### Erreurs possibles:
    - **404**: Utilisateur non trouvé ou profil non trouvé
    - **500**: Erreur serveur
    
    ### Réponse:
    - **204**: Suppression réussie (pas de contenu)
    """
    try:
        # Vérifier que l'utilisateur existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'ID {user_id} non trouvé"
            )
        
        # Récupérer le profil
        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun profil trouvé pour l'utilisateur {user_id}"
            )
        
        # Supprimer le profil
        db.delete(db_profile)
        db.commit()
        
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la suppression du profil: {str(e)}"
        )
