# InstaKiloGram
Projekt realizowany w ramach przedmiotu Projekt Programistyczny 
## Opis:
Kopia instagrama...
## Wymagania funkcjonalne:
- logowanie do aplikacji
- rejestracja do aplikacji
- przeglądanie zdjęć innych użytkowników
- przeglądanie profilu innych użytkowników
- zarządzanie kontem
- like, komentarze
- panel administratora do zarzadzania zarejestrowanymi użytkownikami

## Technologie:
- front - bootstrap
- backend - python, django, mysql/postgresql

## Uruchomienie projektu:
#### 1. Tworzymy wirtualne środowisko:

    virtualenv venv

#### 2. Uruchamiamy utworzone środowisko:
    
    source venv/bin/activate

#### 3. Instalujemy zależnosci:
    
    pip install -r requirements.txt

#### 4. Zmienimay nazwę pliku:
        
    .env.example       
        
na

    .env

#### 5. Ustawiamy zmienne środkowiskowe w pliku **.env**:
    
    SECRET_KEY=change_me
           
Najprościej wygenerować go na stronie https://djecrety.ir/
        
    ALLOWED_HOSTS=127.0.0.1
           
   Ustawiemy adres na localhost
   
#### 6. Tworzymy migarcje i migrujemy modele do bazy danych:
        
    python manage.py makemigrations
    python manage.py migrate

#### 7. Tworzymy konto administratora:

    python manage.py createsuperuser
    
#### 8. Uruchmiamy server:
    
    python manage.py runserver
