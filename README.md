# Lego-Mindstorms-Line-Follower
Code of Robot Lego Mindstorms Line Follower

1.Teoretyczny opis algorytmu podążania za linią:

a)Uchyb regulacji
Algorytm został oparty o dyskretną implementację algorytmu PID. 
Informację o uchybie uzyskujemy za pomocą czujników koloru - mierzą one jasność podłoża pod sobą. Uchyb jest obliczany według wzoru:

e = Cl - Cp

gdzie Cl i Cp to wskazania lewego i prawego czujnika
przy czym wartość zadana zawsze jest równa 0 (zależy nam, aby różnica pomiędzy wskazaniami czujników bywa zerowa - czyli są albo równo "ciemne", albo równo "jasne". Jeżeli z jednej strony odczytujemy jasny kolor, a z drugiej ciemny, to znaczy, że zjechalismy z linii i potrzebujemy na nią wrócić  

 
b)regulacja i co na jej podstawie jest wykonywane
Algorytm PID zwraca regulację, którą należy rozdystrybuować na silniki według wzoru:

|u| = a*( S_w - S_z)

gdzie S_w to silnik wewnętrzny, S_z - silnik zewnętrzny, a to pewna stała, zwana w kodzie "Regulation factor"

Regulacja może być przeznaczona albo na spowolnienie silnika wewnętrznego, albo na przyspieszenie zewnętrznego - obydwa sposoby powodują zmianę toru ruchu w odpowiednim kierunku.
Algorytm przeznacza regulację najpierw na spowolnienie silnika wewnętrznego, do pewnej minimalnej prędkości(może być to prędkość ujemna - czyli silnik nie będzie kręcił się do przodu, lecz do tyłu), a jeżeli dalej pozostała nam regulacja do rozdysponowania - przyspieszenie silnika zewnętrznego.

Oczywiście posługując się tylko wartością bezwzględną regulacji nie jesteśmy w stanie określić kierunku, w którym powinniśmy skręcić(czyli inaczej - wykryć, który silnik ma być wewnątrznym, a który zewnętrznym)

c)jak wykrywany jest silnik wewnętrzny
Silnik wewnetrzny jest wykrywany na podstawie znaku regulacji - jeśli regulacja jest ujemna, to silnikiem wewnętrznym jest silnik lewy (S_l), jeśli regulacja jest dodatnia - silnik prawy (S_l). 

d) Szczegóły implementacyjne PIDa

Regulator PID zaimplementowano jako osobną strukturę, nie związaną bezpośrednio z line followerem. 
Regulacja obliczana jest wełdług wzoru:
u = Kp * e + Ki * integral(e) + Kd * derivative(e)

gdzie Kp, Ki i Kd to odpowiednio parametry P I D regulatora

Całka obliczana jest na podstawie n poprzednich iloczynów różniczki czasu i różniczki uchybu. Mierzymy czas pomiędzy poprzednim obliczeniem PIDa a aktualnym(i na podstawie tego uzyskujemy różniczkę czasu), różniczkę uchybu zaś na podstawie poprzedniego uchybu.

Pochodna liczona jest również na podstawie różniczek czasu i uchybu - oczywiście nie ich iloczynu, lecz ilorazu.

e) wykrywanie koloru

Oprócz wykrywania jasności toru, czujniki cyklicznie odpytują, zależnie od stanu, o pewien zadany kolor, którego poszukujemy, np z celu skręcenia po ciężarek. 
Po uzyskaniu informacji o jasności przełączamy czujniki w tryb pomiaru koloru, mierzymy kolor, i wracamy do trybu pomiaru jasności
 
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

Zalety:
a) Rozdzielenie kodu stanów - każdy stan można implementować i testować osobno (dzięki temu udało nam się wyrobić ze wszystkim czasowo)
b) Symetryczność - żadna ze stron robota nie jest pod żadnym względem faworyzowana, dzięki czemu nie mamy problemów przy zakrętach
c) Optymalna odleglość między osią napędu a czujnikami - bardzo ułatwia wchodzenie w ostre zakręty, robot bardzo rzadko zjeżdża z linii
d) Człon całkujący pamięta tylko n ostatnich iloczynów różniczek - dzięki temu wynik członu całkującego nie ma szans urosnąć do przesadnych rozmiarów w niekorzystnym przypadku (np długiego zakrętu w lewo, i nagłym skręcie w prawo)

Wady:
a) Długie ramię podnośnika - przy próbach podnoszenia większego obciążenia robot może się wywrócić, pomimo niskiego środka ciężkości
b) Wykorzystanie wyjątków do przełączania pomiędzy stanami - metoda kosztowna obliczeniowo, przy większej ilośc obliczeń może powodować opóźnienia w pracy robota



5.Opis budowy robota
Robot ma nisko osadzony środek ciężkości, ma wąski rozstaw osi.
Czujniki:
Czujnik odległości: znajduje się na czole robota, używany przy lokalizacji ładunku.
Czujniki odbitego światła: znajdują się na czole robota ok 0.3 cm od linii. Na czas stanu LINE_FOLLOWER są konfigurowane na światło odbite, lewy czujnik w każdym obiegu pętli głównej jest zmieniany na sprawdzanie koloru
                            co po zwala nam wykryć drogi zjazdowe w których znajduje się ładunek.
