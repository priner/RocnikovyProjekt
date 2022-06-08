Ako používať?

Programy je treba spúšťať v priečinku v ktorom sa nachádzajú.
Očakávajú cestu ku súboru s grafom v argumente -graph.


TCovering

príklad použitia:
sage TCovering.py -graph="../Grafy/5FLOW6.50" -printColoring

bez -printColoring to vypíše iba či sa graf dá zafarbiť, ale zafarbenie
samotné nevypíše


FactorCovering.py

príklad použitia:
sage FactorCovering.py -graph="../Grafy/5FLOWE3.34" -factors=5

Argumente -factors urcuje koľkými páreniami chceme pokryť graf,
ak ho neuvedieme, je to 3.


5cycle

príklad použitia:
sage 5cycle.py -graph="../Komponenty5cyklus/5FLOWE3A.34"


Transitions

príklad použitia:
sage Transitions.py -graph="../Komponenty/componentDeangulator2.10"


Formát vstupu

Grafy sú v bratislavskom formáte. Visiace hrany sú reprezentované ako
normálne hrany ktoré končia vrcholom so stupňom 0.

Pre program Transitions za grafom ešte nasleduje riadok s počtom konektorov,
a pre každý konektor riadok s dvoma číslami vrcholov.

Pre program 5cycle je to podobne ako s Transitions, za grafom nasleduje
riadok s číslom pätíc (čo je vždy 1), a potom jeden riadok s päticou
čísel vrcholov.
