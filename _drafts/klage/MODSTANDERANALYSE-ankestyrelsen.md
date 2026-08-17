# Modstanderanalyse — klage til Ankestyrelsen

**Rolle:** Simuleret juridisk rådgiver for Aarhus Kommune, Teknik og Miljø, jf. `.github/agents/kommunal-modstander.md`
**Genstand:** `_drafts/klage/klage-ankestyrelsen.md` (1012 linjer, udkast dateret 6. maj 2026)
**Dato for gennemgang:** 17. august 2026
**Formål:** Finde og lukke huller, før kommunen finder dem.

Sværhedsgrad: 🟢 let at parere · 🟡 sårbar · 🔴 kritisk svaghed

---

## Status pr. 17. august 2026

**✅ ANVENDT i `klage-ankestyrelsen.md`:**

| Fund | Hvad der er gjort |
|---|---|
| 0.1 Forum | Nyt **afsnit 1.2** — hvorfor tilsynet er rette instans (ingen afgørelse at påklage; ikke afskåret af 2018-fristen; 4.7/4.8 omrubriceret til bevis; ingen anden kontrolinstans) |
| 0.2 Håndhævelsespligt | Nyt **afsnit 1.1** — planlovens § 51 citeret ordret + **nyt spørgsmål 11** |
| 0.3 Hjemmelskæde | Afsnit 4.1 citerer nu hele kæden inkl. overgangsbestemmelserne fra bilag 8, s. 6 |
| 1.1 Vilkår 7 afkortet | Rettet begge steder (afsnit 1 og 3.1) |
| 1.2 2016-grundlaget | Nyt underafsnit i 3.1 *"Vilkårets eget beslutningsgrundlag"* + **bilag 37** + **nyt spørgsmål 12**; indarbejdet i afsnit A og i Prissætning; nævnt i resuméet |
| 2.1 Bevisbyrden | Omskrevet til § 51 + officialprincippet; overskrift ændret; alle tre konklusioner omformuleret |
| 2.2 "ønskes"/"bør" | Nyt underafsnit i 3.3 med tre modargumenter |
| 3.1 Nymarksvej | Enten-eller fjernet; indsnævret til motivbeskrivelsen + manglende udskillelse |
| 3.2 B2 § 35 | Ulovlighedspåstand fjernet; omskrevet til basisprojekt-argumentet |
| 3.5 Seiding | Slettet |
| 3.6 Spørgsmål 10 | Omformuleret inden for tilsynets kompetence |
| Del 4 nr. 2, 3, 4 | Bilag 29→21 rettet; dato → TODO begge steder; bilag 9 udskilt fra 16a |
| Del 4 nr. 5, 6, 7 | Henvisninger tilføjet (16c s. 2; 16e; bilag 9 s. 4) |
| Del 5 F12 | Torshøjvej-anerkendelsen indskrevet i konklusionen for vilkår 7 |
| README | Planklagenævnet/§ 60 → Miljø- og Fødevareklagenævnet/§ 58 c |

**⚠️ MARKERET SOM TODO i klagen — kræver GRGs arkiv, kan ikke løses herfra:**

- ~~**Bilag 14's proveniens**~~ — **LØST, med væsentlig sondring.** GRG har oplyst, at **kun bilag 14** (8. april 2026) er fremsendt til samtlige mødedeltagere; **bilag 38** (22. maj 2025) er *ikke* fremsendt til forvaltningen. Indledningen *"Om bilag og henvisninger"* skelner nu udtrykkeligt mellem de to:
  - **Bilag 14** — fremsendt til direktør, byrumschef, rådmand og to byrådsmedlemmer; forvaltningen har haft lejlighed til at gøre indsigelse. Kommunens standardindvending (*"et ensidigt udarbejdet referat"*) er foregrebet.
  - **Bilag 38** — GRGs egen samtidige nedskrivning. Afsnit 4.7 er derfor **omskrevet**, så mønsteret om manglende punktvis stillingtagen nu primært hviler på kommunens *egne skriftlige besvarelser* (bilag 18 og 16b, hvor MTM og Rambøll udtrykkeligt afviser at kommentere), og bilag 38 kun understøtter. I afsnit 3.3 er citatet *"der kommer beplantning"* **erstattet** med kommunens dokumenterede *handlinger* (bilag 4, borgmesterbrevet, beplantningsforslaget), som er stærkere og uafhængige af referatet. Samme citat er fjernet fra tidslinjen.
  - **Resterer:** fremsendelsesdato for bilag 14, samt sætningen om, at der ikke er modtaget indsigelser (kun hvis det er korrekt) — begge markeret som TODO
- ~~**Mødet 22. maj 2025**~~ — **LØST.** Referatet ligger i `assets/giber-ringvej/2025-05-referat-GRG-og-MTM.txt`, er committet, og indeholder citatet ordret. Optaget som **bilag 38** og henvist i afsnit 3.3, 4.7 og tidslinjen. Referatet gav desuden to gevinster: forvaltningens tilkendegivelse *"at der kommer beplantning"* (nu anvendt mod kommunens standpunkt om, at vilkår 2 er opfyldt), og den præcise formulering *"Der blev derfor ikke givet materielle svar på de enkelte punkter"*. Tidslinjens citat *"Der kommer træer"* var ikke kildens ordlyd og er rettet.
  *(Bemærk: filen `klage/40-moeder-og-korrespondance/2025-05-referat-GRG-og-MTM.txt` — slettet fra arbejdstræet — er fejlnavngivet og indeholder april 2026-referatet. Det er den, der gav anledning til den oprindelige fejlslutning; den rigtige fil lå hele tiden i `assets/giber-ringvej/`.)*
- ~~**Prisoverslaget ca. 100.000 kr.**~~ — **LØST og opgraderet.** GRG har tilføjet beplantnings-aktindsigten i `assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/`. Optaget som **bilag 39**. Materialet gav tre ting, klagen ikke havde:
  1. **🔴 Forvaltningens egen bestilling af 7. august 2025** — specialkonsulent Niiranen til Rambøll, cc byrumschefen: *"hvilken beplantning har indgået som forudsætning for projektet og er projektet udført i overensstemmelse hermed"* og *"Men er det bare uforpligtende eksempler i VVM'en eller er det forudsætninger for projektet?"* Forvaltningen kendte altså ikke selv svaret i august 2025 — seks måneder før borgmesteren kategorisk oplyste, at beplantningen *ikke* var forudsat. **Dette er formentlig det stærkeste enkeltdokument i hele vilkår 2-sporet**, fordi det er internt, samtidigt og ikke møntet på borgerne. Indarbejdet som nyt underafsnit i 3.3
  2. **Bestillingen udsprang af GRGs eget faktaark** (vedhæftet mailen) — det samme faktaark, forvaltningen syv måneder senere afviste med, at man *"ikke [havde] kommenteret nærmere"* på det. Skærper afsnit 4.7 betydeligt
  3. **Prisoverslaget dokumenteret ordret:** Klaus Braad 26. sept. 2025 (ca. 100.000 kr. inkl. vildthegn, 20 m bælte, *"vi er afhængig af at det bliver på frivillig basis, da vi ikke kan ekspropriere"*) og Trine Buus Karlsens svar samme dag: *"det skal betales af Giber Ringvejs projektet"*. To nye anbringender bygget herpå: kommunen henfører selv beplantningen til projektets økonomi (uforeneligt med at den ikke var en projektforudsætning), og en bindende VVM-forpligtelse kan ikke opfyldes gennem en foranstaltning, der beror på frivillige lodsejeraftaler
  4. **De indlejrede kortudsnit** er udtrukket af mailene og lagt i `assets/giber-ringvej/klage/`. Forvaltningens **røde markering af 7. august 2025** er nu gengivet som figur i afsnit 3.3 — den falder sammen med Landskabsstrategiens st. 9.200–9.660 *"Vest for Tandervej"* og med den strækning, Rambøll erkender er *"formegentlig fravalgt af økonomiske årsager"*. Tre uafhængige kilder peger dermed på samme sted
  5. **🔴 Supermarkedsudsagnet:** *"Arealet ved Tandervej kan sandsynligvis sælges til en udvikler, som vil bygge et supermarked."* Kommunen overvejer at afhænde netop det areal, hvor den afskærmende beplantning skulle etableres, uden dokumenteret stillingtagen til, hvordan vilkår 2 så opfyldes. Indarbejdet med anmodning til Ankestyrelsen
  6. **Overstregningen af arealudgiften — nedtonet efter selvkritik.** Verificeret: de to "huller" er sorte overstregningsfelter indsat som billeder (77×14 px, VML-navngivet *"Minustegn"*), placeret ved enhedsprisen og ved den samlede forventede arealudgift. Beplantningsudgiften på ca. 100.000 kr. er udleveret.
     **Første formulering overspillede dette og er rettet.** Kommunen oplyser i samme mail, at erhvervelsen må ske ved frivillig aftale — den skal altså forhandle med lodsejerne. At undtage sin egen vurdering af den forventede arealpris er da en nærliggende og saglig undtagelse (hensynet til myndighedens økonomiske interesser/forhandlingsposition). Asymmetrien forklarer sig selv: de 100.000 kr. er et håndværkeroverslag uden forhandlingsværdi, arealprisen *er* forhandlingspositionen. Et anbringende om illoyalitet her ville være let at parere og ville smitte af på klagens bedre punkter.
     **Det der bæres nu:** at kommunen overhovedet *prissatte* foranstaltningen (man prissætter ikke det uforpligtende), at byrumschefen henførte udgiften til vejprojektets økonomi, og at opfyldelsen beror på frivillige lodsejeraftaler. Ingen af delene afhænger af overstregningen. Klagen anfører nu udtrykkeligt, at overstregningen **ikke** gøres gældende som uberettiget, og beder alene Ankestyrelsen indhente det uoverstregne materiale. Den koblede passage i afsnit 4.8 er fjernet
  7. ~~**Udskrifter**~~ — **LØST.** De tre mails er fremstillet som PDF-udskrifter i samme format som bilag 21/22/28 (`Fra / Til / Cc / Dato / Emne / Vedhæftet`, brødtekst inkl. hele tråden, proveniensnote med originalfilnavnet). Indlejrede kortudsnit og **overstregningsfelterne** gengives inline. Klagen henviser nu til udskrifterne; `.msg`-originalerne beror i samme mappe. Filerne er tillige omdøbt til repoets konvention (`YYYY-MM-DD-mail-<slug>`, ASCII)
     *Bemærk verificeret detalje:* det røde kort stammer fra **bestillingsmailen af 7. august 2025** (image002), ikke fra prisoverslaget — samme billede optræder blot igen i den senere tråd (image010). Byte-identitet bekræftet, så figurteksten i afsnit 3.3 er korrekt
- **GRGs egne tal** (Del 3.3) — 6.000 kr./m omformuleret til et spørgsmål til kommunen; DHM-efterprøvningen markeret til bilagsføring

**🔴 UDESTÅENDE — skal håndteres før afsendelse:**

1. ~~**Verificér planlovens § 51**~~ — **LØST.** Bekræftet ordret mod primærkilden, **LBK nr. 572 af 29/05/2024** (retsinformation.dk), stk. 1, 2 og 3 præcis som citeret i klagen. Gennemgangen af lovteksten gav desuden **planlovens § 63, stk. 1** (*"Det påhviler den til enhver tid værende ejer af en ejendom at berigtige et ulovligt forhold"*), som nu er indarbejdet i afsnit 1.1: pligten består i **begge** kommunens roller — som myndighed efter § 51, som ejer/bygherre efter § 63. Det lukker dobbeltrolle-argumentet i afsnit 2.2 retligt.
  **Konsekvensrettelse i README:** den tidligere rettelse (»rette instans er Miljø- og Fødevareklagenævnet«) var for kategorisk. Lovteksten viser, at planlovens § 58 c siden er **ophævet**, og at en afgørelse om tilsyn/håndhævelse efter § 51 påklages til **Planklagenævnet**, jf. § 58, stk. 1, nr. 3 (kun retlige spørgsmål). README angiver nu begge spor med 4-ugers frist efter § 60.
2. **Bilagsliste og mappe-URL'er** (Del 4 nr. 10) — bilag 21 og 28 linker til en mappe, som GitHub Pages ikke serverer
3. **Commit de manglende assets** (Del 4) — ellers 404 på de offentlige links
4. Overvej **F13 facadeisolering** som selvstændigt punkt — er nu inddraget via spørgsmål 12

---

---

## Del 0 — Kommunens første og billigste træk

Forvaltningens første indlæg til Ankestyrelsen handler ikke om vilkår 7. Det er to sider om, hvorfor styrelsen slet ikke skal rejse sagen. Klagen har intet forsvar mod det.

### 0.1 🔴 Klagen argumenterer aldrig for, at Ankestyrelsen er rette forum

> *"Denne anmodning fremsendes til Ankestyrelsens kommunale tilsyn i medfør af kommunestyrelseslovens §48"* (afsnit 1)

Det er hele hjemmelsafsnittet. Kommunen ville svare — og det er fem selvstændige afvisningsgrunde:

1. **Subsidiaritet.** Tilsynet behandler ikke forhold, en særlig klagemyndighed kan tage stilling til. **Verificeret i bilag 8 selv:** klagevejledningen på s. 9 henviser afgørelsen om VVM-tilladelsen, *"herunder fastsættelse af vilkår"*, til **Miljø- og Fødevareklagenævnet**, jf. planlovens § 58 c, stk. 1, nr. 1 og 2. Kommunen vil sige: klageren er ved den forkerte dør.
2. **Opportunitetsprincippet.** Tilsynet afgør selv, om der er *tilstrækkelig anledning* til at rejse en sag. Klagen giver styrelsen ingen grund til at sige ja.
3. **Legalitet, ikke skøn.** Tilsynet prøver ikke faglige vurderinger.
4. **Ikke god forvaltningsskik.** Afsnit 4.7 (passivitet) og 4.8 (aktindsigt) samt spørgsmål 7 og 8 er ombudsmandsstof. Klagen oplyser endda selv, at en ombudsmandsklage forbeholdes (afsnit 4.8 og noten til afsnit 5) — kommunen vil bruge det som argument for, at GRG selv anser forholdet for at høre til hos Ombudsmanden.
5. **Alder og forpasset frist.** De påklagede dispositioner er fra 2019–2023. Klagefristen for VVM-tilladelsen fra 2018 udløb uudnyttet — hvilket `README.txt` selv noterer (*"En tidligere frist for VVM-tilladelsen fra 2018 blev overskredet uden at blive fanget"*). Kommunen vil kalde anmodningen en omgåelse af den forpassede klagefrist.

**Fix (højeste prioritet i hele dokumentet):** Nyt afsnit 1.1, *"Hvorfor det kommunale tilsyn er rette og eneste instans"*, med fire led:

- Klagen angår **ikke** VVM-tilladelsen eller dens vilkår (det siger afsnit 1 allerede) — den angår kommunens **efterfølgende opfyldelse og håndhævelse**. Der foreligger ingen ny afgørelse, og der er derfor ingen klageadgang til Miljø- og Fødevareklagenævnet at benytte. Det er netop fraværet af en afgørelse, der er problemet.
- Anfør udtrykkeligt, at anmodningen ikke søger tilsynet til at efterprøve et støjfagligt skøn, men om kommunen har iagttaget officialprincippet og sin håndhævelsespligt.
- Omrubricér afsnit 4.7 og 4.8 fra selvstændige klagepunkter til **bevis** for, at sagen ikke er oplyst. Overskriftsniveau og formulering skal vise, at de understøtter afsnit 4.1, ikke konkurrerer med det.
- Adressér frist-indvendingen på forkant: forpligtelsen efter vilkår 7 er løbende og ikke opfyldt, og en løbende manglende opfyldelse forældes ikke, fordi tilladelsen ikke blev påklaget i 2018.

### 0.2 🔴 Håndhævelsespligten påberåbes uden paragraf

> *"planloven pålægger planmyndigheden ansvar for at sikre, at VVM-vilkår overholdes."* (afsnit 4.1)

Ingen paragrafhenvisning. Kommunen ville svare: klageren postulerer en tilsyns- og håndhævelsespligt uden at kunne henvise til den.

Det er ærgerligt, fordi hjemlen findes og er stærk. Klagen bør citere planlovens tilsyns- og lovliggørelsesbestemmelser (§ 51 med tilhørende stykker) direkte, med ordlyd. En **pligt** til at foranledige ulovlige forhold lovliggjort er præcis det, der gør sagen til en legalitetssag og ikke en hensigtsmæssighedssag — altså selve svaret på afvisningsgrund nr. 3 ovenfor.

> ⚠️ **Verificér paragrafnummer og gældende affattelse, inden det skrives ind.** Det er den eneste henvisning i klagen, hvor en fejl direkte ville ramme klagens egen kritik i afsnit 4.1 af, at Rambøll arbejdede ud fra en forkert tekst.

### 0.3 🟡 Hjemmelsangivelsen er rigtig, men ufuldstændig — luk hullet

> *"VVM-tilladelsen er meddelt med hjemmel i VVM-bekendtgørelse nr. 1510 af 15. december 2010 under planloven"* (afsnit 4.1)

Dette er **verificeret korrekt** mod bilag 8, s. 6. Men kommunen kan skabe tvivl, fordi en tilladelse fra oktober 2018 umiddelbart ser ud til at ligge efter miljøvurderingslovens ikrafttræden. Tilladelsen forklarer det selv:

> *"Tilladelsen meddeles i henhold til § 2, stk. 4, nr. 2 i Bekendtgørelse nr. 1510 af 15. december 2010 (...) idet projektet, der er anmeldt februar 2009, er omfattet af overgangsbestemmelserne i miljøvurderingslovens § 57, stk. 8, nr. 2, og i VVM-bekendtgørelse nr. 957 af 27. juni 2016, § 17, stk. 2."*

**Fix:** Citér hele kæden inkl. overgangsbestemmelserne. Så er indvendingen død, før den fremsættes.

---

## Del 1 — Det tungeste enkeltfund: vilkår 7 er citeret forkert

### 1.1 🔴 Klagen gengiver ikke vilkår 7 fuldstændigt

Klagen citerer vilkår 7 sådan (afsnit 1, gentaget i afsnit 3.1):

> *"At der suppleres med øget støjdæmpning ved boliger i det åbne land, ved Tranbjerg, ved Mårslet, ved forlængelsen til Beder Landevej og ved Kolt, inden for en økonomisk ramme på ca. 20 mio. kr."*

Vilkåret lyder i bilag 8, s. 3 (verificeret i kilden):

> *"At der suppleres med øget støjdæmpning ved boliger i det åbne land, ved Tranbjerg, ved Mårslet, ved forlængelsen til Beder Landevej og ved Kolt, inden for en økonomisk ramme på ca. 20 mio. kr., **jf. Byrådsbeslutningen den 14. september 2016.**"*

**Kommunen ville svare:** Klageren bruger et helt afsnit (4.1) på at bebrejde Rambøll, at rådgiveren gengav vilkårene i en anden affattelse end den meddelte — og har selv afkortet det vilkår, hele klagen handler om, netop dér hvor det henviser til sit eget beslutningsgrundlag. Det bemærkes, at klageren dermed anlægger en strengere målestok for myndigheden end for sig selv.

Det er en gratis sejr for kommunen, og den koster klagen troværdighed på det sted, hvor den er mest afhængig af den. **Skal rettes, alle steder.**

### 1.2 🔴 Den udeladte henvisning er samtidig klagens stærkeste ubrugte våben

`2016-udvalgs-erklaering.pdf` ligger allerede i `assets/giber-ringvej/`. Det er Teknisk Udvalgs erklæring af 5. september 2016 — grundlaget for byrådsbeslutningen, vilkår 7 henviser til. Den siger:

> *"At den i VVM-en skitserede støjafskærmning **fastholdes og suppleres med** øget støjdæmpning ved Mårslet, Tranbjerg, forlængelsen til Beder Landevej og Kolt, inden for en økonomisk ramme på ca. 20 mio. kr. **Lokalområderne inddrages i en nærmere afklaring af støjafskærmningen.**"*

Klagen nævner 2016 præcis ét sted i 1012 linjer — og kun som en del af et Rambøll-citat. Det er en alvorlig underudnyttelse. Ordlyden afgør fire af klagens omtvistede spørgsmål:

| Ordlyd i 2016-erklæringen | Hvad den afgør |
|---|---|
| *"fastholdes **og** suppleres med"* | **Det VVM-skitserede er basis; puljen er additionen.** Dette er den direkte tekstlige modgift mod hele kommunens og Rambølls forsvar om, at vejsænkning, projektiboende afgravninger og skitseret afskærmning kan tælle med. Argumentet skal ikke længere udledes af ordene "suppleres"/"øget" i vilkåret alene — det står i det dokument, vilkåret selv henviser til. |
| *"Lokalområderne inddrages i en nærmere afklaring af støjafskærmningen"* | En **procedureforpligtelse**, der aldrig er opfyldt. Den underminerer samtidig kommunens forsvar om udokumenteret "borgerdialog": det, der var pålagt, var inddragelse af lokalområderne i en afklaring — ikke en journaliseringsløs samtale med unavngivne borgere (jf. afsnit 3.3 og 3.1 B5). |
| *"At det i VVM-en skitserede længdeprofil ved Giber Å **fastholdes**"* | Udvalget sondrede udtrykkeligt mellem det, der **fastholdes** fra VVM'en, og det, der **suppleres**. Længdeprofil-poster hører til den første kategori. Styrker afsnit A markant. |
| *"tilbydes tilskud til isolering af bygningers facader (...) hvis støjniveauet overstiger 58 dB"* | En selvstændig forpligtelse fra samme beslutning (jf. F13 i FINDINGS). Er den nogensinde tilbudt? Og er udgiften i givet fald henført til de 20 mio. kr.? |

Hertil kommer fra samme dokument, s. 4 — forvaltningens egen oplysning til udvalget i september 2016:

> *"Kommunen har noget overskudsjord, man gerne vil anvende."*

Det er samtidig dokumentation for, at anvendelse af overskudsjord var forudsat allerede ved beslutningen om de 20 mio. kr. Det styrker prissætningsafsnittet: jorden var en forudsætning for løsningen, ikke en merudgift, rammen skulle dække.

**Fix:** Nyt underafsnit i 3.1 — *"Vilkår 7's eget beslutningsgrundlag: 'fastholdes og suppleres med'"* — placeret **før** gennemgangen af de tre redegørelser, så det står som den målestok, posterne herefter måles mod. Fremskaf desuden selve byrådsbeslutningen af 14. september 2016 (referat/indstilling) som selvstændigt bilag; udvalgserklæringen af 5. september er grundlaget, men vilkåret henviser til byrådets beslutning.

---

## Del 2 — Bærende præmisser uden støtte

### 2.1 🔴 Bevisbyrden

> *"Kommunen bærer som planmyndighed bevisbyrden for, at VVM-vilkår er opfyldt."* (afsnit 3.1)

Postuleret uden hjemmel eller praksis. Og **alle tre** konklusionsafsnit hviler på den: *"På det foreliggende grundlag har kommunen ikke løftet bevisbyrden for, at vilkår 2/5/7 er opfyldt."*

**Kommunen ville svare:** Det bestrides, at der i en tilsynssag gælder en omvendt bevisbyrde. Tilsynet rejser sag, når der er grundlag for at antage en ulovlighed; det påhviler den, der gør ulovligheden gældende, at sandsynliggøre den. Klageren konstruerer en bevisbyrderegel og bygger derefter samtlige konklusioner på den.

Vurdering: 🔴 — ikke fordi kommunen har ret, men fordi ét ubegrundet led bærer tre konklusioner. Falder leddet, falder de alle.

**Fix — to spor, brug begge:**
1. **Forankr den.** Officialprincippet + kravet om, at en myndighed skal kunne dokumentere grundlaget for sin egen konstatering af, at et bindende vilkår er opfyldt. Det er ikke en bevisbyrde i civilprocessuel forstand, men et krav til forvaltningsgrundlaget.
2. **Omformulér konklusionerne, så de ikke afhænger af den.** Erstat *"har ikke løftet bevisbyrden"* med det, der faktisk er dokumenteret og uomtvisteligt: *"Kommunen har over for GRG oplyst, at en opgørelse ikke kan udarbejdes, og har ikke fremlagt noget andet grundlag, hvorpå konstateringen af vilkårsopfyldelse hviler."* Den formulering kan kommunen ikke angribe — den er citeret fra kommunen selv (bilag 26, s. 2).

### 2.2 🔴 "ønskes" og "bør" — klagens egne citater er formuleret som hensigter

Afsnit 3.3 citerer VVM-redegørelsen:

> *"Hvor der er nærliggende tæt bebyggelse **ønskes** vejanlægget sløret med en beplantning"*

og Landskabsstrategien:

> *"Grundet visuelle støjgener **bør** dæmningsanlæg (...) skærmes med beplantning tæt på byområder"*

— og behandler dem herefter som eksplicitte krav.

**Kommunen ville svare:** Klageren læser et bindende krav ind i formuleringer, der efter deres ordlyd er ønsker og anbefalinger. Havde VVM-redegørelsen villet fastsætte et krav, ville den have skrevet "skal". Det bemærkes, at klageren i afsnit 4.1 selv anfører, at forskellen mellem *"i mindst 4 meters højde"* og *"ensartet højde (4m)"* ikke er redaktionel — klageren kender altså udmærket betydningen af ordvalg, men anvender princippet selektivt.

Vurdering: 🔴 — dette er kommunens *første* angreb på hele vilkår 2-sporet, og klagen møder det ikke.

**Fix:** Adressér det udtrykkeligt, før kommunen gør det. Tre led:
- **Inkorporationsargumentet:** Vilkår 2 gør anvisningerne bindende ved henvisning. Et vilkår, der pålægger, at anlæggene *"tilpasses (...) i henhold til anvisningerne"*, får sin normative kraft fra vilkåret, ikke fra anvisningernes egen sproglige modus. Anvisninger i et plandokument er netop formuleret som anvisninger — det er henvisningen i vilkåret, der binder dem.
- **Tilladelsens egen begrundelse** (bilag 8, s. 8) opregner beplantning blandt de afbødende foranstaltninger: *"Det landskabelige indgreb afbødes ved afrunding af skråningsanlæg og ved at etablere ny beplantning i sammenhæng med det omgivende landskab."* Det er tilladelsens eget udsagn om, hvad den hviler på — ikke redegørelsens ønske.
- **Konsekvensargumentet:** Hvis "anvisningerne" kun binder, hvor de er formuleret som "skal", er vilkår 2 tomt, for et plandokument formulerer sjældent detailkrav i bydeform.

### 2.3 🟡 Klagen lover ikke at gå ind i faglige skøn — og gør det så

Afsnit 1: *"Det gøres ikke gældende, at Ankestyrelsen skal kontrollere kommunens konkrete faglige støjskøn."*

Men afsnit 3.2 udleder dB-forskelle ved at aflæse en trendlinjefigur (*"forskellen er under ca. ½ dB"*, *"ved nyudlægning (år 0) er SMA8 endog ca. 1 dB mere støjsvag"*), og afsnit 3.1 B5 aflæser *"1–2 dB"* af et effektkorts signaturforklaring.

**Kommunen ville svare:** Klageren erklærer, at sagen ikke angår faglige skøn, og beder derefter tilsynet lægge klagerens egen aflæsning af en trendlinjegraf til grund frem for rådgiverens vurdering. Det er præcis en hensigtsmæssighedsprøvelse.

**Fix:** Behold data, men skift altid det retlige spørgsmål tilbage til dokumentation. Ikke *"KVS giver ikke målbar reduktion"*, men *"kommunen har ikke oplyst, hvilken reduktion i forhold til hvilken referencebelægning den har lagt til grund — og Vejdirektoratets egne data giver anledning til at spørge."* Særligt spørgsmål 4 og 9 i afsnit 5 skal formuleres som dokumentations- og stillingtagenspørgsmål, aldrig som spørgsmål om det rigtige dB-tal.

---

## Del 3 — Enkeltargumenter, der ikke overlever modsvaret

### 3.1 🔴 Nymarksvej-argumentet (afsnit 3.1 B5) har et svar, klagen ikke lukker

> *"Enten er tiltaget udført til opfyldelse af en bindende forpligtelse efter VVM-tilladelsen — og da kan kommunen ikke over for retten anføre, at det ikke sker som følge af en retlig forpligtelse. Eller også er det (...) en frivillig disposition (...) — og da kan det ikke opgøres som anvendelse af puljen."*

**Kommunen ville svare:** Klageren læser et procesindlæg uden for sin sammenhæng. Anbringendet blev fremsat i en naboretlig erstatningssag som svar på sagsøgerens påstand om, at kommunen anerkendte en pligt til at dæmpe støj for naboer. Udsagnet angår, at der ikke bestod en *naboretlig forpligtelse over for den pågældende sagsøger* — ikke at VVM-tilladelsens vilkår 7 ikke findes. De to udsagn er fuldt forenelige. Klagerens "enten-eller" er en falsk modsætning.

Vurdering: 🔴 — argumentet fremstår i dag som klagens skarpeste, og det er det, der falder hårdest, når modsvaret kommer.

**Fix — indsnævr til det, der overlever.** Fjern enten-eller-konstruktionen. Behold:
- Kommunen har over for retten beskrevet anlæggets **motiv** som frivillig aftale og nyttiggørelse af overskudsjord. Det er ikke foreneligt med samtidig at opgøre det som *pligtmæssig* anvendelse af en ramme til *supplerende* støjdæmpning — ikke fordi udsagnene er logisk uforenelige, men fordi kommunen ikke i nogen af sammenhængene har udskilt en merudgift.
- Beløbet er aldrig udskilt. Det står uanset hvilken læsning af procesindlægget man vælger.
- Tilføj forbeholdet selv: *"Det erkendes, at udsagnet er fremsat i en anden retlig sammenhæng. Det påberåbes alene som kommunens egen samtidige beskrivelse af tiltagets baggrund."* Det koster intet og fjerner angrebsfladen.

Samme indsnævring gælder prissætningsafsnittets brug af *"færre omkostninger (...) end ved at flytte jorden"*: en besparelse i forhold til deponi udelukker ikke, at der er en anlægsudgift. Formuleringen *"kan ikke (...) opgøres som et forbrug af puljens ca. 20 mio. kr."* er for stærk — den holdbare version er, at kommunen har beskrevet dispositionen som omkostningsreducerende og aldrig har fremlagt det regnestykke, der forener det med en post på 18,5 mio. kr.

### 3.2 🔴 B2 (Mustrupvej): klagens eget citat modsiger dens påstand

Klagen gør gældende, at jordvolden mangler landzonetilladelse og derfor ikke er lovligt etableret, jf. planlovens § 35 — og citerer i samme afsnit Rambøll:

> *"Det er korrekt at der ikke er en landzonetilladelse, **da volden/adgangsvejen er en del af projektet for at skabe adgang til ejendomme.**"*

**Kommunen ville svare:** Klageren fremlægger selv forklaringen på, hvorfor der ikke er en selvstændig landzonetilladelse — anlægget er en integreret del af det vejprojekt, der er tilladt ved VVM-tilladelsen — og påstår derefter ulovlighed. Det bemærkes, at klageren i afsnit 3.1 B4 anvender nøjagtig samme betragtning (*"en integreret del af vejprojektet"*) til støtte for det modsatte resultat.

Vurdering: 🔴 — en ulovlighedspåstand, der falder på klagens eget bilag, smitter af på de øvrige påstande.

**Fix:** Drop § 35-ulovlighedspåstanden. Brug den konsistente version, som er stærkere og som klagen allerede har materialet til: er volden *"en del af projektet"*, er den pr. definition basisprojekt og kan ikke samtidig udgøre den supplerende støjdæmpning under vilkår 7. Rambølls svar bliver dermed en indrømmelse i stedet for et modargument.

### 3.3 🟡 Klagen kræver dokumentation, den ikke selv leverer

Tre steder fremlægger GRG egne målinger og overslag uden bilag:

| Sted | Udsagn | Problem |
|---|---|---|
| Prissætning | *"Efter GRGs opmåling strækker de 16 volde sig over ca. 3.100 m"* → ca. 6.000 kr./m | Ingen dokumentation af opmålingen. Klagen erkender selv, at prisen drives af m³, ikke af længde |
| 3.1 B5 | *"GRG har uafhængigt efterprøvet hævningen ved (...) Danmarks Højdemodel (...) på tre punkter"* | Ingen angivelse af punkter, koordinater, metode eller bilag |
| 3.3 | *"Trine Buus Karlsen godkendte et prisoverslag på ca. 100.000 kr. for et 20 meter bredt beplantningsbælte"* | Ingen bilagshenvisning — og udsagnet er tilskrevet en navngiven medarbejder |

**Kommunen ville svare:** Klageren stiller krav om efterprøvbar dokumentation, som klageren ikke selv opfylder. Klagerens egne beregninger fremlægges uden metode, uden data og uden bilag.

**Fix:** Enten bilagsfør (opmålingsgrundlag, DHM-koordinater og -datoer, aktindsigtsdokumentet bag prisoverslaget) eller nedton til et rent spørgsmål: *"Kommunen anmodes om at oplyse mængdeopgørelsen bag de 18,5 mio. kr."* Den navngivne tilskrivning skal have bilag eller ud.

### 3.4 🟡 Bilag 14 bærer for meget for et ensidigt referat

Bilag 14 er GRGs eget mødereferat (.txt). Det bærer alene: Seidings *"formålsløst"*, rådmandens afvisning af at svare, Trine Buus Karlsens *"en jordvold altid har en effekt"*, forvaltningens "bakkelandskab"-overvejelse, beplantningsforslagets hul ved Mårslet og rådmandens anmodning om at undersøge det. Det er bærende materiale i afsnit 2.4, 3.1 B, 3.3, 4.3 og 4.7.

**Kommunen ville svare:** Et ensidigt udarbejdet referat, som forvaltningen ikke har godkendt, kan ikke lægges til grund for, hvad ledende medarbejdere har udtalt.

**Fix:** Oplys i bilagsnoten, om referatet blev fremsendt til forvaltningen, hvornår, og om det er bestridt. Er det fremsendt og ikke bestridt, skal det stå eksplicit — så skifter bevisbyrden for indsigelsen. Er det ikke fremsendt: send det nu, med anmodning om bemærkninger, før klagen indgives. Samme forhold gælder referatet fra 22. maj 2025, der citeres i afsnit 4.7 **uden nogen bilagshenvisning overhovedet** — og hvis fil ifølge git-status er slettet fra `assets/`.

### 3.5 🟡 Seiding-passagen koster mere, end den giver

> *"direktør Henrik Seiding (...) kom til Aarhus Kommune fra en stilling som direktør i Rambøll Management Consulting (2011–2018). Det gøres ikke gældende, at dette udgør formel inhabilitet"* (afsnit 4.5)

**Kommunen ville svare:** Klageren fremdrager en direktørs tidligere ansættelse otte år tilbage, erkender i samme sætning, at det ikke er inhabilitet, og fastholder den alligevel. Det er en personrettet antydning uden retligt indhold.

**Fix:** Slet. Det strukturelle argument om dobbeltrollen står stærkere uden. En tilsynsmyndighed reagerer dårligt på antydninger, og passagen giver kommunen mulighed for at karakterisere hele afsnit 4.5 som personrettet frem for saglig.

### 3.6 🟡 Spørgsmål 10 beder om noget, tilsynet næppe kan give

> *"Om en forsvarlig genoptagelse (...) forudsætter uvildig, ekstern sagkyndig bistand"* (afsnit 5, spørgsmål 10)

Tilsynet udtaler sig om lovligheden af kommunens dispositioner; det instruerer ikke kommunen i, hvordan den tilrettelægger sin sagsbehandling eller hvilke rådgivere den bruger. At bede om en afgørelse, myndigheden ikke kan træffe, giver kommunen anledning til at behandle hele anmodningen som fejladresseret.

**Fix:** Omformulér til et lovlighedsspørgsmål: *"Om kommunen lovligt har kunnet lægge en vurdering til grund, der er udarbejdet af den rådgiver, hvis eget arbejde vurderes, uden nogen form for uafhængig efterprøvelse."* Samme indhold, inden for kompetencen.

### 3.7 🟢 Grænseværdi-fejlslutningen — holder, men stram den

Afsnittet er retligt solidt (et additivt krav opfyldes ikke ved at ligge under en tærskel), og klagen gør klogt i selv at afvise, at 58 dB-kortbestillingen var illoyal. Behold den afgrænsning — den er klagens troværdighedsanker. Kommunen kan kun angribe insinuationen, og den er allerede trukket tilbage i teksten.

### 3.8 🟢 De stærkeste punkter — rør dem ikke

Følgende overlever kommunens bedste modsvar, fordi de udelukkende bygger på myndighedens og rådgiverens egne skriftlige ord:

- **Differenskortet** (afsnit 3.1): kommunen blev oplyst om, at kortet ikke kunne aflæses, svarede *"Jeg tænker godt de kan anvendes"*, og fremlagde det som dokumentation. Uangribeligt.
- **"Det er ikke muligt at lave en opgørelse"** (bilag 26, s. 2): kommunens egen erklæring om, at dokumentationen ikke kan tilvejebringes.
- **"Projektindstillingen tilsidesætter ikke krav i hverken VVM-redegørelse eller VVM-tilladelsen"** (bilag 16f): rådgiveren river grundlaget ud af redegørelse 3.
- **Borgmesterens "projektets resterende økonomi" mod Rambølls "ophører med at eksistere"** (afsnit 4.3): to uforenelige udsagn med en måneds mellemrum.
- **Screeningafgørelsen af 26. januar 2022** (bilag 24): kommunens egen samtidige myndighedsafgørelse om, at volden ikke havde dokumenteret støjeffekt og ikke hørte under vilkår 7. Stærkere end enhver senere indrømmelse, fordi den er samtidig og truffet af kommunen selv.
- **Kommunalfuldmagten mod kommunens eget juridiske notat** (afsnit 3.1): forvaltningen påberåber sig et regelsæt, som dens egne jurister syv måneder forinden havde fastslået viger for skreven lovgivning.
- **Landskabsstrategien mod Rambølls eget fravalg** (afsnit 3.3): dokumentet, kommunen påberåber sig som begrundelse, kræver netop den beplantning, der mangler.

---

## Del 4 — Citat- og henvisningsfejl (billige sejre for kommunen)

Kommunens billigste strategi er at vise, at klagerens henvisninger er upålidelige, og derefter undlade at gå ind i realiteten. Følgende er konkret verificeret i teksten:

| # | Sted | Fejl | Rettelse |
|---|---|---|---|
| 1 | Afsnit 1 og 3.1 | Vilkår 7 citeret uden *", jf. Byrådsbeslutningen den 14. september 2016"* | Se Del 1 — **højest prioriteret** |
| 2 | Afsnit 8 (tidslinje) | *"(bilag 2 og 29)"* om det fjernede notatafsnit. Bilag 29 er transportministerens orientering om KVS-asfalt | Skal være **bilag 21** |
| 3 | Hoved og afsnit 8 | Dato **6. maj 2026** — men i dag er 17. august 2026, og bilag 1 linker til et indlæg dateret 2026-08-07 | Opdatér begge steder ved afsendelse |
| 4 | Bilagsliste | **Bilag 9** indeholder både Rambølls kommentering af marts 2026 (som også er bilag 16a) og beplantningsnotatet af august 2025 | Udskil beplantningsnotatet som eget bilagsnummer; alle *"bilag 9, s. 4"* er i dag flertydige |
| 5 | ~l. 147 | *"Beløbene er estimerede efterfølgende, og er ikke udtryk for den eksakte pris"* — ingen henvisning | Tilføj bilag + side |
| 6 | ~l. 177 | *"Differenskortet viser ikke så klart som ønskeligt..."* — ingen henvisning (er bilag 16e) | Tilføj |
| 7 | ~l. 589 | *"formegentlig fravalgt af økonomiske årsager"* gengivet uden henvisning | Tilføj (bilag 9/beplantningsnotatet, s. 4) |
| 8 | Afsnit 3.3 | Prisoverslag ca. 100.000 kr., tilskrevet navngiven medarbejder — ingen henvisning | Bilagsfør eller fjern navnet |
| 9 | Afsnit 4.7 | Hele mødet 22. maj 2025 og citatet *"ikke på mødet at gå ind i en punktvis behandling"* — ingen henvisning; referatfilen er slettet fra `assets/` | Genetablér referatet som bilag, jf. 3.4 |
| 10 | Bilag 21 og 28 | *".msg-filerne beror i samme mappe"* linker til en **mappe-URL** (`.../aktindsigt-20-mio-mails/`) | GitHub Pages viser ikke mappeindeks — linket giver 404. Link til hver fil, eller fjern |

**Publiceringsforhold:** Samtlige 56 refererede asset-URL'er findes i arbejdstræet (kontrolleret maskinelt). Men mindst disse er endnu ikke committet og vil derfor give 404 på det offentlige site, indtil de er pushet:

```
assets/giber-ringvej/2023-04-13-mtm-juridisk-notat-stoejafskaermning.pdf
assets/giber-ringvej/2023-10-13-mtm-svar-til-giber-ringvej-gruppen.pdf
assets/giber-ringvej/klage/2019-landskabsstrategi-st9200-9660-vest-for-tandervej.png
assets/giber-ringvej/klage/2019-vejdirektoratet-kvs-figur1-stoejtrendlinjer-kvs-sma8-sma11-srs.png
assets/giber-ringvej/klage/2026-vvm-figur44-s85-visualisering-tandervej-maarslet.png
assets/giber-ringvej/klage/2026-vvm-principillustration-s243.png
assets/giber-ringvej/klage/stoejkort-2030-torshoejvej-koelsmosevej-fra-50db.png
assets/giber-ringvej/klage/stoejkort-2030-torshoejvej-koelsmosevej-fra-58db.png
```

Filer med æ/ø i navnet kunne ikke afgøres maskinelt (git-kodning) og skal kontrolleres manuelt. Klagen lover udtrykkeligt i afsnittet *"Om bilag og henvisninger"*, at links springer til den citerede side — et dødt link i et bilag, kommunen selv har afgivet, er unødigt.

**Bemærk også:** `README.txt` i denne mappe angiver **Planklagenævnet** og **planlovens § 60** som det betingede klagespor. Bilag 8's egen klagevejledning peger på **Miljø- og Fødevareklagenævnet**, jf. planlovens § 58 c. Filnavnet `klage-miljoe-og-foedevareklagenaevnet-betinget.md` er altså rigtigt, og README er forældet. Det har betydning for den 4-ugers overvågning, README beskriver.

---

## Del 5 — Ubrugt materiale, kommunen ville frygte

Ud over 2016-erklæringen (Del 1.2):

- **F13, facadeisoleringstilskuddet.** Fra samme 2016-beslutning som puljen: *"tilbydes tilskud til isolering af bygningers facader (...) hvis støjniveauet overstiger 58 dB"*. Da vilkår 7 udtrykkeligt omfatter *"boliger i det åbne land"*, og 2016-erklæringen knytter facadetilskuddet til netop *"spredt bebyggelse i åbent land"*, er spørgsmålet, om tilbuddet nogensinde er givet — og om udgiften er henført til de 20 mio. kr. Enten er det en uopfyldt forpligtelse, eller også er det en post, der mangler i regnskabet. Begge svar gavner klagen.
- **F11, effektkortet måler kun i 1,5 m højde** og indeholder poster (støttemur, støjdæmpende autoværn), der ikke optræder i puljeopgørelsen. Understøtter, at opgørelsen ikke er udtømmende.
- **F12, Torshøjvej-voldene** fremstår som ægte tilføjelser (*"der ikke var indeholdt i det oprindelige projektforslag"*). **Medtag dem udtrykkeligt som poster, der formentlig kvalificerer.** Det koster to sætninger og fjerner kommunens mest effektive karakteristik af klagen — at GRG afviser alt. En klage, der selv anerkender de gyldige poster, er væsentligt sværere at afvise som forudindtaget.

---

# Bryder karakter — samlet vurdering

## ✅ Robust (rør dem ikke)

- Differenskortet fremlagt trods kendt uegnethed
- Kommunens egen erklæring om, at en opgørelse ikke kan udarbejdes
- Screeningafgørelsen af 26. januar 2022 (samtidig myndighedsafgørelse)
- Rambøll: *"Projektindstillingen tilsidesætter ikke krav i (...) VVM-tilladelsen"*
- Borgmester mod rådgiver om, hvorvidt der resterer midler
- Kommunalfuldmagten mod kommunens eget juridiske notat
- Landskabsstrategien mod Rambølls fravalg
- Fejlnummereringen af vilkårene i redegørelse 1 (afsnit 4.1)
- Grænseværdi-fejlslutningen — med den selvvalgte afgrænsning

## ⚠️ Sårbar (skal strammes)

- Faglig-skøn-fælden i afsnit 3.2 og 3.1 B5 → skift til dokumentationsspørgsmål
- GRGs egne udokumenterede beregninger (6.000 kr./m, DHM, prisoverslag)
- Bilag 14 som ensidigt referat + det manglende maj 2025-referat
- Seiding-passagen → slet
- Spørgsmål 10 → omformulér inden for kompetencen
- Enslev/Nymarksvej-argumenternes for stærke formuleringer

## 🔴 Skal omskrives før afsendelse

1. **Vilkår 7 citeres afkortet** — og den udeladte henvisning til byrådsbeslutningen af 14. september 2016 er samtidig klagens stærkeste ubrugte argument (*"fastholdes og suppleres med"*)
2. **Intet forsvar for, at Ankestyrelsen er rette forum** — subsidiaritet, opportunitet, skøn/legalitet, god forvaltningsskik, forpasset frist
3. **Håndhævelsespligten uden paragraf** (afsnit 4.1)
4. **Bevisbyrdepræmissen uden hjemmel** — bærer alle tre konklusioner
5. **"ønskes"/"bør" i vilkår 2-kilderne** — uadresseret
6. **Nymarksvej-enten-eller** — har et svar, klagen ikke lukker
7. **B2's § 35-ulovlighedspåstand** — modsiges af klagens eget citat
8. **Citatfejlene i Del 4** — særligt bilag 29/21 og datoen

## Anbefalet rækkefølge

1. Ret vilkår 7-citatet og skriv 2016-erklæringen ind (Del 1) — største gevinst, mindst arbejde
2. Skriv afsnit 1.1 om forum og håndhævelsespligt (Del 0)
3. Forankr eller omformulér bevisbyrden (2.1) og imødegå "ønskes"/"bør" (2.2)
4. Indsnævr 3.1, 3.2, slet 3.5, omformulér 3.6
5. Ryd citatfejlene og commit de manglende bilag (Del 4)
6. Overvej F13 og F12 (Del 5)

Punkt 1–3 er de eneste, der ændrer klagens retlige bæreevne. Resten er hærdning.
