# Pràctica de Python i Compiladors - LP Q2 2020-2021

Aquesta pràctica tracta sobre el desenvolupament amb ANTLR4 i Python d'un llenguatge anomenat LOGO 3D i el seu interpret.

Logo3D és un llenguatge inspirat en el llenguatge LOGO, que té com objectiu ensenyar a programar als infants a través del joc i l'experimentació, introduint conceptes de matemàtiques, com ara la geometria i la lògica de forma intuïtiva. logo3D compta amb la modificació de poder generar geometria en 3D.

Per aquest treball s'han desenvolupat els següents fitxers:

## logo3d.g (ANTLR4)

Aquest fitxer conté la gràmatica sense context del llenguatge i amb ell generarem el parser i el lexer i els tokens per poder interpretar el llenguatge.

Per generar-ho utilitzarem aqusta comanda per consola:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor Expr.g
```

Això generarà els arxius: logo3d.tokens, logo3dLexer.py, logo3dLexer.tokens, logo3dParser.py i logo3dVisitor.py.

## visitor.py (Python)

Una vegada tenim una gramàtica construida, falta donar-li context i significat a les instruccions que hem creat a logo3d.g. Per això crearem el visitor.py que heredarà de logo3dVisitor.py per implenetar les seves funcions.

Aquí trobarem l'especfiació del llenguatge, on consultarà la funcionalitat de cada crida. Les assignacions, consultes, operacions, procediments... estan  definits al visitor. La seva funció és visitar l'arbre de sintaxis per interpretar les crides del llenguatge mentre es llegeix i després fer l'acció indicada.

Per això, tenim una funció per cada cas indicat al logo3d.g.

## logo3d.py (Python)

A aquest arxiu tenim un scrpit que processa l'arribada per consola a interpretar i que utilitza el nostre visitor per, com ja hem dit, visitar l'arbre generat amb ANTLR4 anterioriment.

## turtle3d.py (Python)

Aquest arxiu conté la classe tutrle3D que és l'encarregada de la generació de les figures geomètriques que volguem crear amb el nostre llenguatge logo 3D.

La nostra torturga té diferents funcions:
- show(): La tortuga, mentre es mou, pinta.
- hide(): La tortuga, mentre es mou, no pinta.
- left(): La tortuga gira en direcció esquerra els graus especificats.
- right(): La tortuga gira en direcció dreta els graus especificats.
- up(): La tortuga gira en direcció cap a dalt els graus especificats.
- down(): La tortuga gira en direcció cap a baix els graus especificats.
- forward(): La tortuga es mou en la direcció que està la distància especificada cap endavant
- backward(): La tortuga es mou en la direcció que està la distància especificada cap enrere.
- home(): Porta la tortuga al origen de coordenades.
- color(): indica quin color volem que pinti la tortuga.

## generació de l'interpret

Una vegada tenim tots els fitxers, només necessitem utilitzar la següent comanda per consola per iniciar l'interpret tot passant un arxiu .l3d que contindrà el codi del nostre llenguatge logo 3D.

```bash
python3 logo3d.py programa.l3d
```

Per definició, el primer procediment a executar-se es el main, si volem executar-ne un altre, haurem d'especificar-lo amb els seus paràmetres de la següent manera:

```bash
python3 logo3d.py programa.l3d quadrats 10 20
```

## Llibreries
Les llibreries utilitzades han estat:

- `vpython` per fer els gràfics 3D.

- `ANTLR` per escriure la gramàtica i l'intèrpret.

- `math` per la utilització de funcions matemàtiques al turtle.py.

- `sys` per llegir l'entrada per consola al logo3d.py.

- `queue` per utilitzar una pila amb LifoQueue al visitor.py.

Al fitxer `requeriments.txt` es poden trobar les llibreries necessaries per aquesta pràctica i la manera d'instal·lar-ho.

```bash
pip install -r requirements.txt
```

## Autor
Alexandre Alemany Orfila

[alexao8](https://github.com/alexao8)
