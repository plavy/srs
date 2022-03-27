# Tajnik - centralni upravitelj lozinki

## Zahtjevi

- Python 3 (optimalno 3.8)

## Korištenje

Prije upotrebe potrebna je inicijalizacija Tajnika koja će generairati potrebne datoteke.
Prilikom inicijalizacije potrebno je zadati proizvoljnu glavnu lozinku koju je nužno koristiti prilikom svake daljnje interakcije.

```shell
python tajnik.py init <masterPassword>
```

> Inicijalizacija poništava prethodno stanje Tajnika.

Nakon toga, moguće je dodavati i dohvaćati lozinke za pojedine stranice.

```shell
python tajnik.py put <masterPassword> <site> <password>
```

```shell
python tajnik.py get <masterPassword> <site>
```

## Sigurnosne specifikacije

### Enkripcija lozinki
Sve lozinke spremeljene su u rječnik. Rječnik se enkriptira u cjelini.
Korištena je simetrična enkripcija AES-128 u modu CBC.
Time je osigurana povjerljivost adresa i lozinki. Nije moguće saznati broj ni duljinu lozinki.
Inicijalizacijski vektor pohranjen je jednostavno u base64 obliku. Zaštita njega nije ključna.

### Zaštita integriteta

Integritet je zaštićen principom Encrypt-then-MAC.
Enkriptirani podaci o lozinkama provedeni su kroz HMAC algoritam koji koristi SHA-256.
Ključ za HMAC različit je od ključa za AES.
HMAC oznaka pohranjena je neenkriptirana. Ona se provjerava prilikom čitanja postojeće loznke i pohrane nove lozinke. 

### Derivacija glavne lozinke

Glavna lozinka derivirana je u dva različita ključa, za AES i HMAC.
Za to je korišten scrypt algoritam s parametrima:
- salt: konstantan
- duljina ključa: 16 bajtova
- CPU: 2^16
- veličina bloka: 8 bajtova
- paralelizacija: 1

### Provjera glavne lozinke

Dodatno, implementirana je jednostavna provjera kompleksnosti glavne lozinke.
Tajnik ne dopušta lozinku kraću od 8 znakova, a upozorava ukoliko lozinka nema posebne znakove.