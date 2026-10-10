RPZ Python Assignment Templates & Solutions

Tento repozitář slouží k vypracování úloh z předmětu RPZ. Využívá konfiguraci dvou vzdálených repozitářů (remotes):

origin: Tvůj osobní (privátní) GitHub repozitář se zálohou řešení.

upstream: Školní FEL GitLab se zadáními a aktualizacemi šablon.

1. Prvotní nastavení (pouze jednou na prvním počítači)

Vytvoř si na svém GitHubu nový privátní repozitář (např. rpz-solutions). Ponech ho prázdný (bez README, licence či .gitignore).

Naklonuj fakultní repozitář a vstup do složky:

git clone git@gitlab.fel.cvut.cz:B201_B4B33RPZ/rpz-python-assignment-templates.git
cd rpz-python-assignment-templates


Přejmenuj výchozí remote ze školního GitLabu na upstream:

git remote rename origin upstream


Přidej svůj GitHub jako nový origin:

git remote add origin git@github.com:<tve-jmeno>/rpz-solutions.git


Vytvoř větev pro svá řešení a nahraj obě větve na svůj GitHub:

# Záloha čistého masteru na GitHub
git push -u origin master

# Vytvoření a nahrání větve s řešeními
git checkout -b solutions
git push -u origin solutions


2. Běžná práce na úkolech

Při vypracovávání úloh pracuj vždy ve větvi solutions:

# Ujisti se, že jsi ve větvi solutions
git checkout solutions

# ... programování a řešení úkolů ...

# Uložení a odeslání na GitHub
git add .
git commit -m "Vypracování úkolu 01"
git push origin solutions


3. Aktualizace zadání v průběhu semestru

Vyučující v průběhu semestru přidávají nová zadání a opravy chyb. Před zahájením práce na novém úkolu stáhni změny:

# 1. Stáhni nová zadání ze školního GitLabu do masteru
git checkout master
git pull upstream master

# 2. Nahraj aktuální master i na svůj GitHub (volitelné, pro udržení čisté zálohy)
git push origin master

# 3. Zamerguj nová zadání do své větve s řešeními
git checkout solutions
git merge master

# 4. Nahraj aktualizovaná řešení na GitHub
git push origin solutions


Poznámka k merge konfliktům: Pokud jsi upravoval stejný soubor, který byl aktualizován v šabloně, Git tě upozorní na konflikt. Konflikt vyřeš v editoru, ulož soubor a dokonči proces pomocí git add . a git commit -m "Merge template update".

4. Práce na novém / jiném počítači

Pokud přejdeš na jiný stroj (např. notebook, lab počítač), postupuj následovně:

Krok 1: Klonování ze svého GitHubu

git clone git@github.com:<tve-jmeno>/rpz-solutions.git
cd rpz-solutions


Krok 2: Přepnutí do větve solutions

git checkout solutions


Krok 3: Propojení se školním GitLabem

Jelikož klon z GitHubu nastaví jako remote pouze origin, je nutné znovu jednorázově přidat školní GitLab jako upstream:

git remote add upstream git@gitlab.fel.cvut.cz:B201_B4B33RPZ/rpz-python-assignment-templates.git


Ověření nastavení

Zkontroluj výpis příkazem:

git remote -v


Měl bys vidět:

origin    git@github.com:<tve-jmeno>/rpz-solutions.git (fetch)
origin    git@github.com:<tve-jmeno>/rpz-solutions.git (push)
upstream  git@gitlab.fel.cvut.cz:B201_B4B33RPZ/rpz-python-assignment-templates.git (fetch)
upstream  git@gitlab.fel.cvut.cz:B201_B4B33RPZ/rpz-python-assignment-templates.git (push)


Po tomto nastavení na novém počítači pokračuješ standardně podle Sekce 2 a Sekce 3.