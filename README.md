# Lego-Mindstorms-Line-Follower
Code of Robot Lego Mindstorms Line Follower

1.Teoretyczny opis algorytmu podążania za linią:

2.Opis implementacji
Stanowość

Robot zawsze znajduje się w jednym z poniższych stanów:
	LINE_FOLLOWER
	FIND_TAKING_LINE
	ENTER_TAKING_LINE_FOLLOWER
	INSIDE_TAKING_FIELD
	EXIT_TAKING_LINE_FOLLOWER
	FIND_EXIT_TAKING_LINE
	FIND_LEAVING_LINE
	ENTER_LEAVING_LINE_FOLLOWER
	LEAVING_BOX
	END

Przy implementowaniu stanów skorzystaliśmy z State design pattern (https://en.wikipedia.org/wiki/State_pattern).
Robort posiada stan który zmienia sie w ciągu dzialania programu i cala odpowiedzialnosc za akcje jest w poszczegolnych stanach.
Stan robota jest obiektem tworzonym kiedy robot wchodzi w stan i niszczonym kiedy go opuszcza

3. Sposób dobierania parametrów algorytmów i przeprowadzania badań.
Nastawy robota badaliśmy empirycznie. Przy nastawap regulacji PID skorzystaliśmy z metody Zieglera-Nicholsa
(https://pl.wikipedia.org/wiki/Regulator_PID#II_Metoda_Zieglera-Nicholsa). Przy regulowaniu poszczególnych stanów
testowaliśmy działanie w poszczególnym stanie i patrzyliśmy do jakiego stanu przechodził następnie robot.

4. Zalety oraz wady rozwiązania

5.Opis budowy robota
Robot ma nisko osadzony środek ciężkości, ma wąski rozstaw osi.
Czujniki:
Czujnik odległości: znajduje się na czole robota, używany przy lokalizacji ładunku.
Czujniki odbitego światła: znajdują się na czole robota ok 0.3 cm od linii. Na czas stanu LINE_FOLLOWER stą konfigurowane
                            na światło odbitę, lewy czujnik w każdym obiegu pętli głównej jest zmieniany na sprawdzanie koloru
                            co po zwala nam wykryć drogi zjazdowe w których znajduje się ładunek.