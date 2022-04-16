# Usermgmt - upravitelj korisnika

## Zahtjevi

- Python 3 (optimalno 3.8)

## Korištenje

Prije svega, potrebno je dodati korisnke u sustav. To omogućava naredba `add`.
Potrebno je unijeti lozinku za korisnika te ju ponoviti.

```shell
python usermgmt.py add <user>
```

Sada se korisnik može prijaviti na sustav koristeći Login.

Moguće je promijeniti lozinku korisnika koristeći `passwd`. Potrebno je unijeti lozinku za korisnika te ju ponoviti.

```shell
python usermgmt.py passwd <user>
```

Ukoliko administrator želi forsirati promjenu lozinke za nekog korisnika, koristit će `forcepass`.
Korisnik će morati upisati novu lozinku prilikom sljedeće prijave.

```shell
python usermgmt.py forcepass <user>
```

Moguće je i obrisati korisnka sa sustava koristeći `del`. Korisnik se više neće moći prijaviti.

```shell
python usermgmt.py del <user>
```

## Sigurnosne specifikacije

### Tajnost lozinki
Program koristi datetoku za pohranu lozinki.
U datoteci je JSON rječnik koji za ključeve ima imena korisnika, a kao vrijednost ima dodatne informacije.
Dodatne informacije su rječnik koji sadrži hash vrijednost lozinke, salt korišten za hashiranje te zastavicu za forsiranje promjene lozinke.
Salt duljine 32 bajta se iznova nasumično generira prilikom svakog hashiranja, odnosno svake pohrane nove lozinke.
Sam salt nije kriptiran, no on garantira da će sve hash vrijednosti biti različite, čak i za iste lozinke, što osigurava njihovu tajnost.

# Login - korisnički prijavitelj

## Zahtjevi

- Python 3 (optimalno 3.8)

> Program se treba nalaziti u istom direktoriju kao i Usermgmt.
> Ovo ograničenje uvedeno je zbog jednostavnosti izrade vježbe kako bi se što manje kopirao kod.
> Naravno, lako je moguće potpuno razdvojiti programe kopiranjem zajedničkih funkcija, ukoliko bi bilo potrebno.

## Korištenje

Prilikom prijave korisnik upisuje svoje ime te potom lozinku.

```shell
python login.py <user>
```

Ukoliko ime korisnika ili lozinka nisu točni, program daje još 2 šanse prije nego što prekine s radom.

Ukoliko administrator forsira promjenu lozinke za korisnika, korisnik će morati unijeti novu loziku prije uspješne prijave.

## Sigurnosne specifikacije

### Siguran unos lozinke
Loznika se ne unosi zajedno s naredbom poziva programu, već ju program naknadno traži.
Prilikom unosa lozinke ništa se ne šalje natrag na terminal.
Na ovaj način unesena lozinka ne ostaje u logovima sustava.