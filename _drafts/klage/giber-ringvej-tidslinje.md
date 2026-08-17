---
title: "Giber Ringvej: En tidslinje"
author: Giber Ringvej Gruppen
categories: vejstøj
---

<style>
  .timeline-wrap {
    font-family: Georgia, 'Times New Roman', serif;
    max-width: 720px;
    margin: 0 auto;
    color: #111;
  }

  .timeline-kicker {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c00;
    margin-bottom: 0.4rem;
  }

  .timeline-headline {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 2.6rem;
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 0.5rem 0;
    color: #111;
  }

  .timeline-deck {
    font-size: 1.1rem;
    color: #444;
    line-height: 1.55;
    border-top: 3px solid #111;
    border-bottom: 1px solid #ccc;
    padding: 0.9rem 0;
    margin-bottom: 2.5rem;
  }

  /* --- Sporoversigt --- */
  .tracks {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.4rem;
    margin: 0 0 2.6rem 0;
  }

  @media (max-width: 620px) {
    .tracks { grid-template-columns: 1fr; gap: 1rem; }
  }

  .track {
    border-top: 3px solid #111;
    padding-top: 0.7rem;
  }

  .track--beplantning { border-top-color: #4a7c59; }
  .track--belaegning  { border-top-color: #3d5a80; }
  .track--pulje       { border-top-color: #c00; }

  .track-nr {
    display: block;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.66rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.2rem;
  }

  .track-name {
    display: block;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.02rem;
    font-weight: 700;
    line-height: 1.2;
    color: #111;
    margin-bottom: 0.5rem;
  }

  .track-req {
    font-size: 0.82rem;
    line-height: 1.5;
    color: #555;
    margin: 0 0 0.6rem 0;
  }

  .track-status {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.78rem;
    line-height: 1.45;
    color: #111;
    margin: 0;
    padding-top: 0.5rem;
    border-top: 1px solid #e5e5e5;
  }

  .track-status strong { color: #c00; }

  /* --- Spormarkering på tidslinjeposter --- */
  .tl-spor {
    display: inline-block;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #666;
    border-left: 3px solid #bbb;
    padding: 0.05rem 0 0.05rem 0.45rem;
    margin-bottom: 0.35rem;
  }

  .tl-spor--beplantning { border-left-color: #4a7c59; color: #4a7c59; }
  .tl-spor--belaegning  { border-left-color: #3d5a80; color: #3d5a80; }
  .tl-spor--pulje       { border-left-color: #c00;    color: #c00; }
  .tl-spor--proces      { border-left-color: #888;    color: #777; }

  .tl {
    position: relative;
    padding-left: 0;
    margin: 0;
    list-style: none;
  }

  .tl::before {
    content: '';
    position: absolute;
    left: 5.8rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #111;
  }

  .tl-item {
    display: flex;
    gap: 1.6rem;
    margin-bottom: 0;
    position: relative;
  }

  .tl-date {
    flex: 0 0 5.6rem;
    text-align: right;
    padding-top: 1.1rem;
  }

  .tl-year {
    display: block;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    color: #111;
    line-height: 1;
  }

  .tl-month {
    display: block;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    margin-top: 0.15rem;
  }

  .tl-dot {
    flex: 0 0 auto;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #111;
    border: 2px solid #fff;
    box-shadow: 0 0 0 2px #111;
    margin-top: 1.35rem;
    position: relative;
    z-index: 1;
  }

  .tl-dot.red {
    background: #c00;
    box-shadow: 0 0 0 2px #c00;
  }

  .tl-dot.open {
    background: #fff;
  }

  .tl-body {
    flex: 1;
    padding: 0.9rem 0 1.8rem 0;
    border-bottom: 1px solid #e5e5e5;
  }

  .tl-item:last-child .tl-body {
    border-bottom: none;
  }

  .tl-tag {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #c00;
    display: block;
    margin-bottom: 0.25rem;
  }

  .tl-title {
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0 0 0.4rem 0;
    color: #111;
  }

  .tl-text {
    font-size: 0.9rem;
    color: #444;
    line-height: 1.6;
    margin: 0;
  }

  .tl-text em {
    font-style: italic;
    color: #333;
  }

  .tl-fig {
    margin: 1rem 0 0.3rem 0;
  }

  .tl-fig img {
    width: 100%;
    height: auto;
    display: block;
    border: 1px solid #ddd;
    background: #fff;
  }

  .tl-fig figcaption {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.72rem;
    line-height: 1.45;
    color: #777;
    margin-top: 0.45rem;
  }

  .tl-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 0.5rem 0 0.5rem 7.4rem;
  }

  .tl-divider-label {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #aaa;
    white-space: nowrap;
  }

  .tl-divider-line {
    flex: 1;
    height: 1px;
    background: #ddd;
  }

  .kladde-banner {
    border: 2px solid #c00;
    background: #fff8f8;
    padding: 0.85rem 1.1rem;
    margin-bottom: 1.6rem;
  }

  .kladde-banner p {
    margin: 0;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.85rem;
    line-height: 1.5;
    color: #333;
  }

  .kladde-banner strong {
    display: block;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #c00;
    margin-bottom: 0.3rem;
  }

  .timeline-footer {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 3px solid #111;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    color: #666;
  }
</style>

<div class="timeline-wrap">

<div class="kladde-banner">
  <p><strong>Kladde — under udarbejdelse</strong>
  Denne tidslinje er et arbejdsdokument, der løbende opdateres i takt med, at sagens materiale gennemgås. Enkelte forhold er endnu ikke endeligt afklaret, og fremstillingen kan blive ændret. Den tilhørende anmodning til Ankestyrelsen er ikke indgivet.</p>
</div>

<p class="timeline-kicker">Sagen om Giber Ringvej</p>
<h1 class="timeline-headline">De 20 millio&shy;ner ingen kan gøre rede for</h1>
<p class="timeline-deck">
  Aarhus Kommune fik i 2018 en VVM-tilladelse til Giber Ringvej på tre bindende vilkår: slørende beplantning, støjdæmpende vejbelægning og en pulje på <em>ca. 20 mio. kr.</em> til øget støjdæmpning. Otte år senere fastholder kommunen, at alle tre er opfyldt. Men beplantningen mangler dér, hvor den var forudsat, asfalten dæmper ikke målbart mere end en standardbelægning — og om puljen skriver forvaltningen selv, at det <em>"ikke [er] muligt at lave en opgørelse af, hvad omkostningerne til de besluttede tiltag reelt har været."</em>
</p>

<div class="tracks">

  <div class="track track--beplantning">
    <span class="track-nr">Vilkår 2</span>
    <span class="track-name">Slørende beplantning</span>
    <p class="track-req">Anlægget skal tilpasses landskabet <em>"i henhold til anvisningerne i VVM redegørelsen"</em> — og de foreskriver beplantning, hvor vejen passerer tæt bebyggelse.</p>
    <p class="track-status"><strong>Status:</strong> Ikke etableret ved Mårslet. Der ses ingen dokumenteret afgørelse om at fravige vilkåret.</p>
  </div>

  <div class="track track--belaegning">
    <span class="track-nr">Vilkår 5</span>
    <span class="track-name">Støjdæmpende vejbelægning</span>
    <p class="track-req">Hele vejanlægget skal udformes med støjdæmpende vejbelægning. Projektet forudsatte ifølge Rambøll en SRS-belægning.</p>
    <p class="track-status"><strong>Status:</strong> Der er udlagt KVS. Hverken referencebelægning, type eller dokumenteret støjreduktion er oplyst.</p>
  </div>

  <div class="track track--pulje">
    <span class="track-nr">Vilkår 7</span>
    <span class="track-name">Pulje på ca. 20 mio. kr.</span>
    <p class="track-req">Der skal <em>suppleres</em> med øget støjdæmpning ved Tranbjerg, Mårslet, Kolt, forlængelsen til Beder Landevej og i det åbne land.</p>
    <p class="track-status"><strong>Status:</strong> Intet særskilt regnskab. Flere påberåbte tiltag er af rådgiveren erkendt ikke at være støjtiltag.</p>
  </div>

</div>

<ul class="tl">

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2014</span>
      <span class="tl-month">Dec</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Planlægning</span>
      <p class="tl-title">VVM-redegørelsen i offentlig høring</p>
      <p class="tl-text">Miljøkonsekvensvurderingen for Bering-Beder vejen — Tillæg 43 til Kommuneplan 2013 — sendes i offentlig høring (1. december 2014 – 28. februar 2015). <a href="/assets/giber-ringvej/2013-vvm.pdf#page=77">Redegørelsen</a> undersøger tre linjeføringer og forudsætter, at vejen lægges lavt i terrænet og sløres med beplantning, hvor den passerer tæt forbi byområderne: <em>"Hvor der er nærliggende tæt bebyggelse ønskes vejanlægget sløret med en beplantning, så den visuelle støj begrænses"</em> (s. 77). Det er disse anvisninger, VVM-tilladelsens vilkår 2 senere gør bindende.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2026-vvm-principillustration-s243.png" alt="Principillustration fra VVM-redegørelsen: et bælte af ny beplantning placeret mellem Bering-Beder vejen og husene i bysamfundet.">
        <figcaption>VVM-redegørelsen, figur 17.3 (s. 243): <em>"Den visuelle støj fra vejen sløres med beplantning ved bysamfundene."</em> Beplantningsbæltet er tegnet ind mellem vejen og husene.</figcaption>
      </figure>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2026-vvm-figur44-s85-visualisering-tandervej-maarslet.png" alt="Terrænvisualisering fra VVM-redegørelsen: udsigten fra Mårslet langs Tandervej mod syd, med træbeplantning langs den kommende vej.">
        <figcaption>Figur 44 (s. 85): <em>"Visualisering af udsigt fra Mårslet langs Tandervej mod syd med beplantning langs Bering-Beder vejen, som vil sløre bilerne i landskabet."</em> Visualiseringer som denne blev opstillet flere steder i Mårslet under VVM-processen — det var dette projekt, borgerne tog stilling til.</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2016</span>
      <span class="tl-month">Sep</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Planlægning</span>
      <p class="tl-title">Byrådet vælger linjeføring A — og afsætter 20 mio. kr.</p>
      <p class="tl-text">Byrådet vælger den nordlige linjeføring A — den, der går tættest på bysamfundene Mårslet og Tranbjerg — og vedtager Kommuneplantillæg 43, der formaliserer projektet. Med byrådsbeslutningen den 14. september 2016 afsættes samtidig rammen på <em>ca. 20 mio. kr.</em> til øget støjdæmpning, på grundlag af <a href="/assets/giber-ringvej/2016-udvalgs-erklaering.pdf#page=1">Teknisk Udvalgs erklæring</a>: <em>"At den i VVM-en skitserede støjafskærmning fastholdes og suppleres med øget støjdæmpning ved Mårslet, Tranbjerg, forlængelsen til Beder Landevej og Kolt, inden for en økonomisk ramme på ca. 20 mio. kr."</em> Ordet <em>suppleres</em> er centralt: puljen skal lægges oven i den afskærmning, projektet i forvejen indeholdt. Forløbet er beskrevet i den <a href="/assets/giber-ringvej/2016-kommunalplan-tillaeg-sammenfattende-redegoerelse.pdf">sammenfattende redegørelse</a>.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2018</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-tag">Borgermøde</span>
      <p class="tl-title">Borgermøde forud for VVM-tilladelsen</p>
      <p class="tl-text">Borgermøde i Grønlykkehallen med fremmødte fra Beder, Mårslet, Tranbjerg, Kolt/Hasselager og de øvrige bysamfund langs den kommende vej. Efter deltagernes gengivelse blev der givet tilsagn om, at vejen ikke ville give støjproblemer af betydning. Mødet er medtaget her som baggrund; det er ikke dokumenteret ved referat, og der støttes ikke ret på det.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2018</span>
      <span class="tl-month">Okt</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-tag">Juridisk grundlag</span>
      <p class="tl-title">VVM-tilladelse udstedt — fire vilkår bliver sagens kerne</p>
      <p class="tl-text">
        Aarhus Kommune udsteder den 12. oktober <a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=2">VVM-tilladelsen</a> på i alt 18 vilkår. Fire af dem angår støj og landskab:<br>
        <strong>Vilkår 2</strong> — <em>"Udformningen af de samlede anlæg – veje, skråningsanlæg, støjvolde, beplantning mv - tilpasses det omgivende landskab ... i henhold til anvisningerne i VVM redegørelsen."</em> Vilkåret gør dermed VVM-redegørelsens anvisninger bindende — og de specificerer beplantning som sløringstiltag ved tæt bebyggelse.<br>
        <strong>Vilkår 5</strong> — Hele det nye vejanlæg, inklusiv forbindelsen fra Oddervej til Beder Landevej, skal udformes med støjdæmpende vejbelægning og med støjafskærmning langs nordsiden ved Tranbjerg.<br>
        <strong>Vilkår 6</strong> — Landevejen skal have støjdæmpende asfalt, og støjafskærmningen langs Landevejen skal udføres <em>"i mindst 4 meters højde i begge vejsider"</em> fra Ingerslevvænget forbi Tingskovparken.<br>
        <strong>Vilkår 7</strong> — Der skal <em>suppleres</em> med øget støjdæmpning ved boliger i det åbne land, ved Tranbjerg, ved Mårslet, ved forlængelsen til Beder Landevej og ved Kolt — <em>"inden for en økonomisk ramme på ca. 20 mio. kr."</em>
      </p>
      <p class="tl-text">Tilladelsens egen begrundelse fastslår, at vilkårene <em>"har til formål at sikre gennemførelsen af foranstaltninger, der kan afhjælpe projektets virkninger på omgivelserne"</em> — og nævner udtrykkeligt, at det landskabelige indgreb afbødes <em>"ved at etablere ny beplantning i sammenhæng med det omgivende landskab"</em>. Det er ikke hensigtserklæringer, men betingelser tilladelsen er meddelt på. Skellet mellem vilkår 5, 6 og 7 bliver afgørende: de to første pålægger afskærmning kommunen under alle omstændigheder skal levere — det sidste kræver noget <em>ud over</em> det.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2019</span>
      <span class="tl-month">Jan</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Intern beslutning</span>
      <p class="tl-title">Rambølls "Landskabsstrategi" udarbejdes</p>
      <p class="tl-text">Rambøll udarbejder den 24. januar en intern <a href="/assets/giber-ringvej/2019-landsskabstrategi.pdf">Landskabsstrategi</a> — oversigtsplanen der omsætter VVM-vilkår 2's beplantningskrav til konkrete tiltag for hver delstrækning. Dokumentet planlægger "Visuel støjskærmning (beplantning) nordside af vej" specifikt ved stationering 9.200–9.660 — strækningen vest for Tandervej ved Mårslet, som Rambøll i sit senere beplantningsnotat betegner Tandervej–Mustrupvej. Strategiens overordnede principafsnit fastslår desuden, at <em>"dæmningsanlæg, der ligger hævet over terræn, bør skærmes med beplantning tæt på byområder"</em>. Dokumentet er internt og bliver først udleveret til borgerne syv år senere, efter gentagne aktindsigtsanmodninger. Pointen viser sig da at være den modsatte af kommunens. Den slørende beplantning, VVM-redegørelsen forudsatte ved bysamfundene, står ikke etableret noget sted langs vejen. Og på strækningen vest for Tandervej — hvor Landskabsstrategien oven i købet nævner den eksplicit — erkender Rambøll i sit <a href="/assets/giber-ringvej/2025-08-notat-redegørelse-for-beplantning.pdf#page=4">eget notat</a>, at <em>"beplantning er formegentlig fravalgt af økonomiske årsager"</em>. Det dokument, forvaltningen påberåber sig som grundlag for detailprojekteringen, foreskriver altså netop det, der mangler.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2019-landskabsstrategi-st9200-9660-vest-for-tandervej.png" alt="Udsnit af Landskabsstrategiens tiltagsliste for strækningen St. 9.200-9.660 &quot;Vest for Tandervej&quot;. Blandt de opregnede tiltag står &quot;Visuel støjskærmning (beplantning) nordside af vej&quot;.">
        <figcaption>Landskabsstrategiens egen tiltagsliste for strækningen <strong>St. 9.200–9.660 "Vest for Tandervej"</strong> ved Mårslet. Femte punkt er <em>"Visuel støjskærmning (beplantning) nordside af vej"</em>. Netop om denne strækning erkender Rambøll syv år senere, at <em>"beplantning er formegentlig fravalgt af økonomiske årsager"</em>. Kilde: <a href="/assets/giber-ringvej/2019-landsskabstrategi.pdf">Landskabsstrategien</a> (bilag 20).</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2019</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Landzonetilladelse</span>
      <p class="tl-title">Kommunen giver tilladelse til en støjvold på én meter</p>
      <p class="tl-text">Den 27. maj meddeler Aarhus Kommune <a href="/assets/giber-ringvej/2019-05-27-landzonetilladelse-stoejvold-nymarksvej.pdf#page=2">landzonetilladelse</a> til støjvolden "S8" mellem Tandervej og Nymarksvej ved Mårslet. Rambøll havde ansøgt tre uger forinden om <em>"en støjvold Mellem Tandervej og Nymarksved ved Mårslet"</em>, der <em>"nedbringer støjen fra vejanlægget på de nærliggende bebyggelser"</em>. Tilladelsen begrundes med hensynet til <em>"at begrænse støjpåvirkningen af omkringliggende ejendomme"</em>.</p>
      <p class="tl-text">Målene står i ansøgningen: volden er <em>ca. 750 meter lang</em>, har en <em>2 meter bred top</em> og ligger <em>1 meter over terræn</em>, med skråningsanlæg 1:2 mod vejen og 1:10 på bagsiden. Syv år senere beskriver Rambøll det samme anlæg som <em>dyrkningsskråninger</em>, hvis formål <em>"netop er at de ikke er synlige i landskabet"</em> — og over for Retten i Aarhus forklarer kommunen, at volden ikke blev etableret som følge af nogen retlig forpligtelse, men efter <em>"en frivillig aftale med lodsejeren"</em>.</p>
      <p class="tl-text">GRG spørger i marts 2023 skriftligt, om netop S8 er etableret. Spørgsmålet er efter det oplyste aldrig besvaret — skønt svaret lå i kommunens egne sagsakter.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2019</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Politisk beslutning</span>
      <p class="tl-title">Byrådet godkender projektindstilling — med "bl.a."</p>
      <p class="tl-text">Byrådet godkender den 28. august <a href="/assets/giber-ringvej/2019-08-06-projektgodkendelse.pdf#page=5">projektindstillingen</a>, der opregner eksempler på, hvad puljens 20 mio. kr. kan bruges til. Formuleringen lyder: <em>"bl.a."</em> — et ord, der siden hen bliver genstand for central uenighed. Forvaltningen hævder listen er udtømmende. GRG fastslår, at "bl.a." pr. definition er eksemplificerende.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2020</span>
      <span class="tl-month">Mar</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Anlægsbevilling</span>
      <p class="tl-title">Byrådet bevilger anlægget — herefter føres intet regnskab med puljen</p>
      <p class="tl-text">Den 11. marts godkender byrådet anlægsbevillingen til Bering-Beder vejen. Puljen på 20 mio. kr. indgår nu som en post i det samlede anlægsoverslag. Rambøll beskriver senere, hvad der sker derfra: <em>"Herefter føres der ikke separat regnskab med midler anvendt til støjtiltag, men blot jord- og andre arbejder generelt."</em></p>
      <p class="tl-text">Kort efter vejens åbning stopper projektlederen i Teknik og Miljø, og der sker løbende medarbejderudskiftning hos både kommune og rådgiver. Forvaltningen beskriver selv konsekvensen: <em>"vi har manglet en del af indsigten i historikken for projektet, da spørgsmålene vedrørende støj efter vejens åbning skulle besvares"</em> — og at der, da den første opgørelse blev lavet i 2023, <em>"heller ikke på dette tidspunkt [var] opmærksomhed på, at byrådet (...) havde besluttet konkret hvad puljen på 20 mio. kr. skulle anvendes til."</em></p>
      <p class="tl-text">Det er kernen i det, der følger. De opgørelser, kommunen fremlægger fra 2023 og frem, er ikke registreringer af, hvad pengene gik til. Det er rekonstruktioner, lavet bagud af folk der efter forvaltningens eget udsagn ikke kendte beslutningen, de skulle rekonstruere.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2022</span>
      <span class="tl-month">Jan</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Myndighedsafgørelse</span>
      <p class="tl-title">Kommunen afgør selv: jordvolden ved Kølsmosevej er ikke et støjtiltag</p>
      <p class="tl-text">Aarhus Kommune – Plan, Byggeri og Miljø træffer den 26. januar <a href="/assets/giber-ringvej/2022-01-26-screeningafgoerelse-jordvold-koelsmosevej.pdf#page=3">screeningsafgørelse</a> for jordvolden ved Kølsmosevej og konstaterer skriftligt, at <em>"der i projektet ikke er medsendt dokumentation for ej heller lagt vægt på at jordvolden har en støjdæmpende effekt"</em>, hvorfor den <em>"anses primært som et anlæg til bortskaffelse af affald"</em>. Samme dokument fastslår, at volden <em>"ikke [indgik] som en del af VVM-redegørelsen ej heller VVM-tilladelsens vilkår 7"</em>. Dagen efter meddeles <a href="/assets/giber-ringvej/2022-landzonetilladelse-deponivold.pdf#page=1">landzonetilladelsen</a>, der alene nævner <em>visuel afskærmning</em> som formål — støj nævnes ikke med ét ord. Halvandet år senere optræder den samme vold som ét af "16 støjvolde" i puljeregnskabet.</p>
    </div>
  </li>

  <div class="tl-divider">
    <span class="tl-divider-label">Vejen åbner</span>
    <span class="tl-divider-line"></span>
  </div>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2022</span>
      <span class="tl-month">Efterår</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-tag">Åbning</span>
      <p class="tl-title">Giber Ringvej åbner for trafik</p>
      <p class="tl-text">Vejen tages i brug i etaper hen over efteråret (september–december 2022). Den slørende beplantning, VVM-redegørelsen forudsatte ved bysamfundene, er ikke etableret. Vejbelægningen er KVS-asfalt — ikke den støjreducerende SRS-belægning, projektet ifølge Rambøll hele vejen igennem havde forudsat. Da Aarhus Kommune kort efter sender sin støjhandlingsplan i høring, er Giber Ringvej den kommunale vej, der giver anledning til flest høringssvar.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Mar</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Foretræde</span>
      <p class="tl-title">GRG stiller de to spørgsmål, der stadig venter svar</p>
      <p class="tl-text">Den 20. marts har Jane Simonsen foretræde for Teknisk Udvalg på vegne af den nystiftede Giber Ringvej Gruppe. Forvaltningen gengiver dagen efter <a href="/assets/giber-ringvej/aktindsigt-20-mio-mails/2023-03-21-mail-sv-vedr-stoej-fra-giber-ringvej.pdf">internt</a>, at der på mødet blev spurgt ind til påstanden om, at <em>"Giber Ringvej er ikke bygget som godkendelsen i VVM"</em>. I det <a href="/assets/giber-ringvej/2023-03-20-grg-bilag-til-teknisk-udvalg.pdf">fremlagte bilag</a> stilles blandt andet to konkrete spørgsmål: om <em>"der er støjvolde som ikke er etableret (fx ”S8” mellem Tandervej og Nymarksvej)"</em>, og <em>"Der er indskrevet en sum på 20 mill. kr til ”øget støjdæmpning ved boliger i det åbne land”- hvorledes er disse midler anvendt? og hvor?"</em></p>
      <p class="tl-text">Forvaltningen beder samme uge rådgiveren udarbejde et notat til udvalget. Ingen af de to spørgsmål er besvaret i dag — tre et halvt år senere.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Apr</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Internt juridisk notat</span>
      <p class="tl-title">Kommunens egne jurister: kommunalfuldmagten viger for skreven lov</p>
      <p class="tl-text">Den 13. april udarbejder Teknik og Miljøs rådmandssekretariat et <a href="/assets/giber-ringvej/2023-04-13-mtm-juridisk-notat-stoejafskaermning.pdf#page=3">juridisk notat</a> om rammerne for kommunal finansiering af støjafskærmning. Notatet fastslår: <em>"Hvis en kommunal opgavevaretagelse er reguleret i den skrevne lovgivning (love, bekendtgørelser), kan og skal opgavevaretagelsen ikke også have hjemmel i kommunalfuldmagtsreglerne. Kommunalfuldmagtsreglerne viger med andre ord for den skrevne lovgivning."</em></p>
      <p class="tl-text">Notatet angår efter sin egen titel <em>eksisterende</em> veje. Om nyanlæg anfører det, at miljømyndigheden i en VVM-tilladelse <em>"skal (...) fastsætte en række vilkår bl.a. om foretagelse af støjberegninger og gennemførelse af støjbegrænsende tiltag"</em>. Syv måneder senere afviser samme forvaltning yderligere støjdæmpning med henvisning til netop kommunalfuldmagten.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Intern korrespondance</span>
      <p class="tl-title">Notatet redigeres før forelæggelsen — svarene skal gives separat</p>
      <p class="tl-text">Efter GRGs foretræde for Teknisk Udvalg den 20. marts 2023 udarbejder Rambøll et notat til udvalget. Notatets afsnit 4 indeholdt rådgiverens svar på gruppens punkter, og afsnittet fjernes efter forvaltningens instruktion, inden notatet forelægges. Instruktionen — i <a href="/assets/giber-ringvej/aktindsigt-20-mio-mails/2023-05-09-mail-re-stoejmaaler-ved-giber-ringvej.pdf">intern korrespondance frigivet ved aktindsigt</a> — lyder: <em>"Det må dog gerne fremstå lidt mere færdigpoleret. De må også gerne pille afsnit 4 med svarerne på Janes punkter ud (det håndterer vi separat)."</em> Rambøll bekræfter den 9. maj: <em>"Afsnittet omkring besvarelse af spørgsmål er som aftalt fjernet."</em> Begrundelsen er saglig, og et separat svar kommer faktisk — fem måneder senere. Men som det fremgår nedenfor, besvarer det ikke gruppens to tungeste spørgsmål.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Kommunens redegørelse 1</span>
      <p class="tl-title">Rambøll: 16 støjvolde for 17,28 mio. kr.</p>
      <p class="tl-text">Teknik og Miljø fremsender en <a href="/assets/giber-ringvej/2023-08-Ramboll-redegoerelse.pdf#page=1">redegørelse fra Rambøll</a> til Teknisk Udvalg. Notatets samlede opgørelse lyder på 30,53 mio. kr., hvoraf 17,28 mio. kr. henføres til puljen — vilkår 7 dermed opfyldt. Opgørelsen indeholder imidlertid en sænkning af længdeprofilet sydøst for Enslev (4,5 mio. kr.), som Rambøll selv senere kalder <em>"en tracérings-mæssig konsekvens af vejtekniske udfordringer"</em>, en støjskærm langs Landevejen (5,2 mio. kr.) der er hjemlet i vilkår 5 og 6 — ikke i puljen — samt tilkørselsveje, jorddeponier og en vold mod letbanen. Prisen på de 16 volde — 18,5 mio. kr. — er opgjort under ét. Notatet oplyser de enhedspriser, en støjvold prissættes efter, men ingen af de mængder, priserne skal ganges med: hverken areal eller jordvolumen er angivet for nogen af voldene, og de er ikke opregnet enkeltvis.</p>
      <p class="tl-text">Notatet indledes med det, der betegnes som et <em>"udsnit fra VVM-tilladelsen"</em> — men de gengivne vilkår svarer hverken i nummerering eller ordlyd til <a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=2">den tilladelse, kommunen faktisk meddelte</a>. Kravet om støjskærm <em>"i mindst 4 meters højde"</em> er blevet til <em>"ensartet højde (4m)"</em>, kravet om at afskærmningen <em>"skal indpasses i landskabet"</em> er udeladt, og notatet anfører et vilkår om støjvolde ved Tranbjerg, som ikke findes blandt tilladelsens 18 vilkår — forholdet er nævnt i tilladelsens begrundelse, men ikke som et selvstændigt vilkår. Det er ikke ligegyldigt: nedskrivningen fra 30,53 til 17,28 mio. kr. sker netop ved at fjerne <em>"pkt. 8, 9 og 10"</em>, og et af de tre punkter er dette. Hele puljeregnskabet hviler dermed på en anden affattelse af vilkårene end den gældende.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">GRGs svar</span>
      <p class="tl-title">GRG dokumenterer støjproblemet og underkender redegørelsen</p>
      <p class="tl-text">Jakob Aarøe Dam offentliggør et <a href="/2023/08/23/stoej-langs-giber-ringvej--et-modsvar-til-kommunen.html">detaljeret modsvar</a> til Teknisk Udvalg. Analysen viser, at VVM-undersøgelsens støjvurdering ignorerer det store flertal af støjramte borgere, og at Rambølls opgørelse af støjvolde ikke holder. Bemærkelsesværdigt nok opstiller Rambøll i samme redegørelse selv målestokken: <em>"en støjvold skal have en dokumenteret støjdæmpende effekt, ellers kan der ikke opnås tilladelser til at etablere støjvolden."</em> Det er netop den standard, flere af de opgjorte volde ikke lever op til — hvilket kommunen først erkender 17 måneder senere, i januar 2025.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Okt</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Kommunens samlede svar</span>
      <p class="tl-title">Femten svar — men ikke på puljen og ikke på S8</p>
      <p class="tl-text">Den 13. oktober sender Teknik og Miljø et <a href="/assets/giber-ringvej/2023-10-13-mtm-svar-til-giber-ringvej-gruppen.pdf">elleve sider langt svar</a> til Giber Ringvej Gruppen med besvarelse af femten nummererede punkter — om hastighed, fartkontrol, støjmålinger, asfalttype og meget andet. Det er det separate svar, forvaltningen i maj havde varslet.</p>
      <p class="tl-text">Men de 20 mio. kr. er ikke nævnt med ét ord, og støjvolden S8 er ikke nævnt. De to spørgsmål fra marts står fortsat ubesvarede.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Nov</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Forvaltningens svar om økonomien</span>
      <p class="tl-title">“Ikke afregnet” — og kommunalfuldmagten som spærring</p>
      <p class="tl-text">Den 22. november svarer specialkonsulent Rasmus Stougaard Niiranen på GRGs spørgsmål om puljen, jf. <a href="/assets/giber-ringvej/2023-11-22-mtm-svar-pulje-og-kommunalfuldmagt.pdf">mailen</a>. Rammen på de 20 mio. kr. <em>"blev i praksis lagt oveni det samlede udbud af projektet"</em>, og videre: <em>"projektet [har] en samlet økonomistyring, hvor der ikke er afregnet med henblik på præcis opdeling i økonomien for hvert støjdæmpende tiltag. Derudover er projektet fortsat ikke afsluttet og der foreligger derfor ikke et endeligt anlægsregnskab endnu."</em> Rambølls opgørelse betegnes som <em>"en estimering"</em>.</p>
      <p class="tl-text">Det manglende regnskab er altså erkendt allerede her — halvandet år før aktindsigten og to år før den tredje redegørelse. Samme svar afviser yderligere tiltag: <em>"vi [må] på grund af Kommunalfuldmagtsreglerne heller ikke gøre yderligere efter vejen er etableret når grænseværdien på 58dB er overholdt (...) da dette ville kunne ses som begunstigelse af enkeltpersoner"</em> — syv måneder efter kommunens egne jurister havde fastslået, at netop de regler viger for skreven lovgivning.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2024</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-tag">Presse</span>
      <p class="tl-title">Stiften: "Gennembrud i kamp mod vejstøj"</p>
      <p class="tl-text">Aarhus Stiftstidende bringer en <a href="/assets/giber-ringvej/2024-05-23-stiften-gennembrud-i-kamp-mod-vejstøj.pdf">artikel om GRGs arbejde</a> og kampen for støjdæmpning langs Giber Ringvej.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2024</span>
      <span class="tl-month">Sep</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Politisk foretræde</span>
      <p class="tl-title">GRG til foretræde for Støjhandlingsplanen</p>
      <p class="tl-text">GRG <a href="https://dagsordener.aarhus.dk/vis?id=1232cd55-67bf-4142-849b-e59f9c772210&fritekst=støjhandlingsplan&punktid=03d1c259-d0fd-41b3-99c8-cd0b83afd1bf">præsenterer sagen for Teknisk Udvalg</a> og anmoder om et faktatjek af støjvoldenes klassificering og den manglende beplantning. Udvalgsformand Jesper Kjeldsen tilkendegiver: <em>"Vi skal have et faktatjek."</em> Udvalget beder efterfølgende forvaltningen <em>"genbesøge den opgørelse med afsæt i borgerens påstande/spørgsmål"</em>. Rambølls projektchef svarer samme dag internt, at han <em>"er noget i tvivl om hvad vi skal gøre"</em>.</p>
    </div>
  </li>

  <div class="tl-divider">
    <span class="tl-divider-label">Indrømmelserne begynder</span>
    <span class="tl-divider-line"></span>
  </div>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Jan</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Kommunens redegørelse 2</span>
      <p class="tl-title">MTM erkender: estimatet var "misvisende" — men fastholder konklusionen</p>
      <p class="tl-text">Den 13. januar svarer forvaltningschef Michael Tolstrup i <a href="/assets/giber-ringvej/2025-01-mtm-redegoerelse-2.pdf#page=1">redegørelse 2</a>. Tre centrale erkendelser: (1) Rambølls rapport giver et <em>"misvisende billede"</em>, (2) der har <em>"ikke været økonomistyring med henblik på efterfølgende opgørelse af økonomi anvendt til støjdæmpning"</em> — altså intet separat regnskab, og (3) at <em>"det var misvisende, at det fremgik, at der var etableret 16 støjvolde, da ikke alle jorddepoterne er anlagt som deciderede støjvolde"</em>. Som erstatning sendes et <em>"differenskort"</em> over jordniveauforskelle — et kort GRG ikke kan tyde, og som forvaltningen ikke forklarer. Konklusion uændret: vilkårene er overholdt.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Feb</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">GRGs svar</span>
      <p class="tl-title">"De 19 millioner der forsvandt" — GRG underkender redegørelse 2</p>
      <p class="tl-text">GRG offentliggør <a href="/vejst%C3%B8j/2025/02/25/de-19-millioner-der-forsvandt.html"><em>De 19 millioner der forsvandt</em></a> og dokumenterer, at jordvolde bygget af overskudsjord ifølge <a href="/assets/vejstoej-forslag-2024/trafikstoej-kraever-handling-2020.pdf#page=46">branchens egen hvidbog</a> (som Rambøll er medforfatter af) kan etableres for <em>"meget små eller ingen omkostninger"</em>, og at puljens reelle indhold derfor er langt mindre end opgjort. <a href="/assets/giber-ringvej/2025-01-29-vejdirektoratet-stavtrup-jordvold-oekonomi.txt">Vejdirektoratet bekræfter senere</a>, at en støjvold af overskudsjord er billigere end at køre jorden til deponi. GRG drøfter sagen med borgmester Anders Winnerskjold, som beder forvaltningen udarbejde en ny redegørelse. Sagen omtales i <a href="https://dinavis.dk/samfund/ECE18005991/borgere-klager-over-trafikstoej-fra-giber-ringvej-hvad-blev-der-af-de-20-mio-kr">Din Avis</a> og <a href="https://stiften.dk/debat/vi-undrer-os-her-ved-giber-ringvej-19-millioner-kroner-er-aabenbart-forsvundet">Aarhus Stiftstidende</a>. Teknisk Udvalg <a href="https://dagsordener.aarhus.dk/vis?id=ebd4c6d2-8061-409e-91e3-90451978c7c3&punktid=6cc3391e-d693-4bb7-8ad8-8be08de5f2eb">orienteres den 5. marts</a>.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Apr</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Kommunens redegørelse 3</span>
      <p class="tl-title">MTM: byrådet afgjorde det i 2019 — sagen lukket</p>
      <p class="tl-text">Den 2. april sender forvaltningen <a href="/assets/giber-ringvej/2025-04-02-redegoerelse-3-mail.pdf#page=1">redegørelse 3</a> til GRG. Ny strategi: projektindstillingen fra 2019 skal have <em>endeligt afgrænset</em> puljens anvendelse. De fire godkendte tiltag er: (1) vejsænkning, (2) støjvolde ved byområder, (3) støjvæg i Tranbjerg, (4) flytning af vej syd for Oddervej. Konklusion: <em>"der er ikke grundlag for yderligere støjafskærmende tiltag langs Giber Ringvej."</em> GRG identificerer straks fire fejl: vejsænkning var i VVM-grundprojektet fra 2013, støjvæggen er hjemlet i vilkår 5 og 6 — ikke i puljen under vilkår 7, vejflytningen skete af oversigts- og sikkerhedshensyn, og projektindstillingens ordlyd bruger <em>"bl.a."</em> — der pr. definition ikke er udtømmende.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">GRGs svar</span>
      <p class="tl-title">GRG piller redegørelse 3 fra hinanden — faktaark for faktaark</p>
      <p class="tl-text">GRG offentliggør fire faktaark der systematisk dokumenterer svaghederne i kommunens tre redegørelser: <a href="/assets/giber-ringvej/2025-05-faktaark-pulje-til-oeget-stoejdaempning-redegoerelse-1.pdf">Redegørelse 1</a>, <a href="/assets/giber-ringvej/2025-05-faktaark-pulje-til-oeget-stoejdaempning-redegoerelse-2.pdf">Redegørelse 2</a>, <a href="/assets/giber-ringvej/2025-05-faktaark-pulje-til-oeget-stoejdaempning-redegoerelse-3.pdf">Redegørelse 3</a> og <a href="/assets/giber-ringvej/2025-05-faktaark-beplantning-som-afvaergeforanstaltning.pdf">beplantning som afværgetiltag</a>. Faktaarkene sendes til Rambøll for kommentering.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Aktindsigt · gentagne forsøg</span>
      <p class="tl-title">Rambøll har hele tiden givet GRG ret — forvaltningen fortiede det</p>
      <p class="tl-text">Efter <em>gentagne enslydende aktindsigtsbegæringer</em> dukker en mail frem med GRGs høringssvar annoteret af Rambøll. Det <a href="/assets/giber-ringvej/2025-05-faktaark-pulje-til-oeget-stoejdaempning-redegoerelse-2-efter-aktindsigt.pdf">annoterede dokument</a> viser, at Rambøll skriftligt tiltræder GRGs indsigelser om fire af tiltagene: Letbanevolden, Mustrupvej-volden, Testrup-volden og Ingerslevvej-deponiet kan ikke medregnes som støjtiltag. Ingen af disse forbehold fremgår af det sammenfatningsnotat, kommunen fremsendte som sit officielle svar — hvor konklusionen tværtimod er, at puljens anvendelse har været korrekt.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Jun</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-tag">Presse · Debat</span>
      <p class="tl-title">Stiften-kronik: Rådmanden gør ingenting</p>
      <p class="tl-text">GRG <a href="/vejst%C3%B8j/2025/06/04/hastighedsnedsaettelser-tillaeg-til-indstilling.html">fremlægger for Teknisk Udvalg</a>, at hastighedsnedsættelser kan reducere støj og uheld markant. Fulgt op af kronik i Stiften: <a href="https://stiften.dk/debat/vi-ved-hvad-der-virker-alligevel-goer-raadmanden-ingenting"><em>Vi ved, hvad der virker — alligevel gør rådmanden ingenting</em></a>. Rådmanden svarer i juli: <a href="https://stiften.dk/debat/jeg-har-selv-silkeborgvej-udenfor-mit-sovevaerelse-men-farten-skal-kun-ned-hvor-det-giver-mening"><em>Farten skal kun ned, hvor det giver mening</em></a> — og begrunder bl.a. afvisningen med risiko for kødannelse. Rådmanden beklager efterfølgende i mail til GRG og erkender, at man ikke kan sætte lighedstegn mellem hastighedsnedsættelser og kødannelse.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Intern bestilling · Aktindsigt</span>
      <p class="tl-title">Forvaltningen spørger sin egen rådgiver: er beplantningen overhovedet et krav?</p>
      <p class="tl-text">Den 7. august skriver specialkonsulent Rasmus Stougaard Niiranen til Rambøll, med byrumschef Trine Buus Karlsen som kopimodtager, og bestiller den redegørelse, der bliver til notatet nedenfor. <a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-08-07-mail-bestilling-af-redegoerelse-for-beplantning.pdf">Bestillingen</a> — frigivet ved aktindsigt — lyder: <em>"Der skal redegøres for om beplantning er sket i overensstemmelse med VVM'en. Eller med andre ord hvilken beplantning har indgået som forudsætning for projektet og er projektet udført i overensstemmelse hermed."</em></p>
      <p class="tl-text">Og videre, med et kortudsnit indsat i mailen: <em>"Her kunne det fx godt ligne, at der er lagt op til afskærmende beplantning ud for Mårslet omkring området markeret med rødt nedenfor. <strong>Men er det bare uforpligtende eksempler i VVM'en eller er det forudsætninger for projektet?</strong>"</em></p>
      <p class="tl-text">Mailen er intern og ikke skrevet til borgerne. Den viser, at forvaltningen i august 2025 ikke selv havde taget stilling til det spørgsmål, hele sagen handler om — og at den var i tvivl om netop den sondring, kommunen siden afviser. Seks måneder senere svarer borgmesteren kategorisk, at beplantningen <em>"ikke [var] forudsat etableret som en del af VVM-tilladelsen eller projektgodkendelsen"</em>. Hvad der i mellemtiden afklarede spørgsmålet, fremgår ikke af det fremlagte materiale.</p>
      <p class="tl-text">Bestillingen har desuden GRGs eget <a href="/assets/giber-ringvej/2025-05-faktaark-beplantning-som-afvaergeforanstaltning.pdf">faktaark om beplantning</a> vedhæftet — det ark, forvaltningen syv måneder senere besvarer med, at man <em>"ikke [har] kommenteret nærmere på dette faktaark."</em> Arket var altså tilstrækkeligt til at få kommunen til at bestille en redegørelse hos sin rådgiver, men blev over for afsenderen afvist som ikke værd at kommentere.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2025-08-07-mtm-bestilling-roed-markering-vest-for-tandervej.png" alt="Luftfoto med rød markering langs nordsiden af Giber Ringvej umiddelbart vest for Tandervej ved Mårslet.">
        <figcaption>Forvaltningens eget kortudsnit fra bestillingsmailen af 7. august 2025. Det røde område ligger langs nordsiden af vejen vest for Tandervej — <strong>samme strækning</strong>, som Landskabsstrategien seks år tidligere udpegede med <em>"Visuel støjskærmning (beplantning) nordside af vej"</em>, og hvor Rambøll erkender, at beplantning er <em>"formegentlig fravalgt af økonomiske årsager"</em>.</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Rambøll-notat · Beplantning</span>
      <p class="tl-title">Træerne blev sparet væk — og ingen kan sige hvem der besluttede det</p>
      <p class="tl-text">Den 19. august udarbejder Rambøll et <a href="/assets/giber-ringvej/2025-08-notat-redegørelse-for-beplantning.pdf#page=4">notat om beplantning</a> på opdrag af Aarhus Kommune. Notatet gennemgår forløbet fra VVM-redegørelse til detailprojekt og afslører to kritiske forhold for to nabostræninger:</p>
      <p class="tl-text"><strong>St. 9.200–9.660 (vest for Tandervej, Damgårdstoften):</strong> Landskabsstrategien planlagde eksplicit <em>"Visuel støjskærmning (beplantning) nordside af vej"</em>. Beplantning er aldrig etableret. <a href="/assets/giber-ringvej/2025-08-notat-redegørelse-for-beplantning.pdf#page=4">Rambølls forklaring</a>: <em>"Beplantning er formegentlig fravalgt af <strong>økonomiske årsager</strong>."</em> Aarhus Kommune kan ikke fremlægge referat eller dokumentation for denne beslutning.</p>
      <p class="tl-text"><strong>St. 9.660–10.320 (øst for Tandervej):</strong> Rambøll begrunder fravalget med, at borgergrupper ønskede udsigt over markerne mod syd — en kommunikation der <em>"er foregået mellem Aarhus kommunes projektleder og de relevante borgergrupper <strong>uden om Rambølls involvering</strong>."</em> Der ses ikke fremlagt journaliseret dokumentation for, hvem der deltog i denne dialog, hvornår den fandt sted, eller hvem der traf den endelige beslutning. En lokal dialog kan under alle omstændigheder ikke i sig selv fravige et bindende VVM-vilkår — det kræver en dokumenteret afgørelse fra planmyndigheden, og en sådan ses ikke truffet i nogen af de to tilfælde.</p>
      <p class="tl-text">Dermed står forløbet klart: beplantningen blev forudsat i VVM-redegørelsen, visualiseret for borgerne, gjort bindende ved vilkår 2 og konkretiseret strækning for strækning i Landskabsstrategien — for til sidst at blive <em>"formegentlig"</em> fravalgt, uden at nogen myndighed har truffet og journaliseret en beslutning om det. Kommunens eget svar til GRG i oktober 2025 medgiver, at der er <em>"to områder langs Giber Ringvej omkring Mårslet, hvor der ud fra VVM-rapporten kunne argumenteres for en forventning om, at der skulle etableres afskærmende beplantning"</em> — men tilføjer, at det ikke fremgår <em>"som tydelige krav."</em></p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Sep</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Intern beslutning · Aktindsigt</span>
      <p class="tl-title">Prisen på de manglende træer: ca. 100.000 kr.</p>
      <p class="tl-text">Den 26. september kl. 8.36 skriver Klaus Braad til byrumschef Trine Buus Karlsen, jf. <a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-09-26-mail-vs-redegoerelse-for-beplantning-prisoverslag.pdf">mailen frigivet ved aktindsigt</a>: <em>"Har snakket med Gorm og han siger at det vil koste ca. 100.000,- inkl. vildt hegn. Han foreslår at det bliver en blanding af løvtræer og buske (...) Jeg foreslår at der laves et bælte på 20 meter i bredden, som vist herunder, men vi er afhængig af at det bliver på frivillig basis, da vi ikke kan ekspropriere til arealerne."</em></p>
      <p class="tl-text">Samme dag kl. 14.58 svarer Trine Buus Karlsen: <em>"Vil du sætte dette projektet i gang og <strong>det skal betales af Giber Ringvejs projektet</strong>."</em></p>
      <p class="tl-text">To ting følger heraf. For det første prissætter man ikke en foranstaltning, man anser for uforpligtende — og udgiften henføres udtrykkeligt til vejprojektets egen økonomi. For det andet beror løsningen på frivillighed: kommunen oplyser selv, at den ikke kan ekspropriere til arealerne. Et bindende VVM-vilkår kan vanskeligt anses for opfyldt gennem en foranstaltning, hvis gennemførelse afhænger af, om private lodsejere vil sælge — og der ses ingen redegørelse for, hvad kommunen gør, hvis aftalerne ikke opnås.</p>
      <p class="tl-text">Mailen slutter: <em>"Arealet ved Tandervej kan sandsynligvis sælges til en udvikler, som vil bygge et supermarked, hvis det er tilfældet så bliver arealet væsentligt dyrere."</em> Det areal, der er tale om, er efter forvaltningens egen markering i august netop det sted, hvor den afskærmende beplantning skulle stå.</p>
      <p class="tl-text">De beregnede beløb for selve arealerhvervelsen er overstreget i det udleverede materiale; udgiften til beplantningen er derimod udleveret. Kommunen oplyser i samme mail, at erhvervelsen må ske ved frivillig aftale, og hensynet til myndighedens forhandlingsposition kan efter omstændighederne begrunde overstregningen — men det er dermed uoplyst, hvad foranstaltningen samlet er anslået at koste.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Nov</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-tag">Presse · Debat</span>
      <p class="tl-title">Stiften-kronik: Vi mangler ikke viden — kun vilje</p>
      <p class="tl-text">GRG publicerer et <a href="/vejst%C3%B8j/2025/11/10/faktaark-vejstoej-og-effekt-af-hastighedsnedsaettelser.html">detaljeret faktaark</a> om vejstøj og effekten af hastighedsnedsættelser i Aarhus. Fulgt op af kronik i Stiften: <a href="https://stiften.dk/debat/vi-mangler-ikke-viden-kun-vilje-saenk-farten"><em>Vi mangler ikke viden — kun vilje — sænk farten</em></a>.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Jan</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Politisk henvendelse</span>
      <p class="tl-title">Sagen forelægges borgmesteren</p>
      <p class="tl-text">Den 21. januar forelægger GRG sagen for borgmester Anders Winnerskjold. Han tilkendegiver, at kommunen vil se på den — et tilsagn, der giver fornyet håb om en reel behandling.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Feb</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Afslag · Triggerdokument</span>
      <p class="tl-title">Borgmesteren afviser at genoptage sagen</p>
      <p class="tl-text">Trods tilsagnet fra januar fastholder borgmester Anders Winnerskjold den 25. februar kommunens tre hidtidige redegørelser og afviser en samlet genoptagelse. Det er reelt et afslag på at foretage en korrekt og fuldstændig retlig stillingtagen til, om VVM-vilkårene er opfyldt — og det bliver det formelle triggerdokument for klagen til Ankestyrelsen.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Mar</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Rambølls svar på faktaarkene</span>
      <p class="tl-title">Rambøll: intet separat regnskab — og rammen er "blot en omtrentlig angivelse"</p>
      <p class="tl-text">Den 25. marts kommenterer Rambøll <a href="/assets/giber-ringvej/2026-03-ramboell-kommentering-af-faktaark.pdf#page=3">GRGs faktaark</a>. Notatet indeholder tre centrale erkendelser: <em>"Herefter føres der ikke separat regnskab med midler anvendt til støjtiltag, men blot jord- og andre arbejder generelt"</em>; at sænkningen sydøst for Enslev sker <em>"som en tracérings-mæssig konsekvens af vejtekniske udfordringer"</em> og <em>"ikke i sit primære sigte er et støjmæssigt tiltag"</em>; og at de tiltag, der er udført ved Nymarks Allé, er <em>dyrkningsskråninger</em> med hældning 1:10, hvis formål <em>"netop er at de ikke er synlige i landskabet"</em>.</p>
      <p class="tl-text">Samtidig omfortolkes beløbsrammen: prisen på tiltagene er ifølge Rambøll <em>"myndigheden uvedkomne"</em>, og at rammen nævnes i tilladelsen <em>"har derfor ikke nogen konsekvens for hvordan midlerne anvendes, men er blot en omtrentlig angivelse"</em>. For første gang henføres desuden KVS-belægningens merpris til puljen — en post, der ikke optræder i nogen af de tre redegørelser. Det er svært at forene med forvaltningens egen påstand om, at puljens anvendelse blev endeligt fastlagt i 2019.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Apr</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--belaegning">Spor · Vejbelægning</span>
      <span class="tl-tag">Vilkår 5 · Vejbelægningen</span>
      <p class="tl-title">Den støjdæmpende asfalt, der ikke dæmper støj</p>
      <p class="tl-text">I <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-1-vvm-giber-ringvej.pdf">afklaringsnotat 1</a> rejser GRG vilkår 5 formelt med tre spørgsmål: Hvilken referencebelægning er lagt til grund? Hvilken KVS-type er udlagt? Og hvilken dokumenteret støjreduktion kan lægges til grund? Baggrunden er, at Rambøll <a href="/assets/giber-ringvej/2026-03-ramboell-kommentering-af-faktaark.pdf#page=3">selv oplyser</a>, at projektet hele vejen igennem forudsatte en støjreducerende belægning — <em>"den typisk valgte belægning til dette formål er en SRS"</em> — men at der i stedet blev udlagt KVS, klimavenligt slidlag.</p>
      <p class="tl-text"><a href="/assets/giber-ringvej/2019-08-vejdirektoratet-kvs-asfalt.pdf#page=4">Vejdirektoratets egne måledata</a> viser, at KVS og standardbelægningen SMA8 følges tæt gennem hele levetiden — og at SMA8 ved nyudlægning endda er den mest støjsvage af de to. Den reduktion på ca. 2 dB, notatet fremhæver, er målt mod den grovere SMA11, ikke mod SMA8, som i dag udgør ca. 70 % af statsvejnettet. Ingen af de tre spørgsmål er besvaret — hverken af Rambøll eller af forvaltningen.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Apr</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--proces">Spor · Sagsbehandling</span>
      <span class="tl-tag">Dialogens sammenbrud</span>
      <p class="tl-title">Møde med MTM: "Vi er juridisk uenige"</p>
      <p class="tl-text">Den 8. april mødes GRG og MTM på rådmandens kontor. GRG fremlægger tre afklaringsnotater om <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-1-vvm-giber-ringvej.pdf">VVM</a>, <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-2-20-mio-giber-ringvej.pdf">puljen</a> og <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-3-sloerende-beplantning-giber-ringvej.pdf">beplantning</a>. Direktør Henrik Seiding erklærer, at parterne er <em>"juridisk uenige"</em>, og at det er <em>"formålsløst at fortsætte med at sende notater frem og tilbage"</em>. Rådmand Nicolaj Bang afviser at svare på, om projektindstillingens liste er udtømmende. GRG varsler klage — <a href="/assets/giber-ringvej/2026-04-referat-GRG-og-MTM.txt">læs referatet</a>.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <span class="tl-tag">Aktindsigt · Beplantning</span>
      <p class="tl-title">Landskabsstrategien i hænde: beplantning var planlagt — og fravalgt uden dispensation</p>
      <p class="tl-text">Efter ny aktindsigtsbegæring udleveres endelig <a href="/assets/giber-ringvej/2019-landsskabstrategi.pdf">Landskabsstrategien fra 24. januar 2019</a> — det interne planlægningsdokument der omsatte VVM-vilkår 2 til konkrete beplantningsplaner for hver delstrækning. Sammenholdt med Rambølls beplantningsnotat fra august 2025 er beviskæden nu komplet: <strong>(1)</strong> VVM-redegørelsen krævede slørende beplantning ved tæt bebyggelse, <strong>(2)</strong> Landskabsstrategien planlagde det konkret — <em>"Visuel støjskærmning (beplantning) nordside af vej"</em> ved st. 9.200–9.660 vest for Tandervej, <strong>(3)</strong> beplantningen blev ikke etableret på netop den strækning, og Rambøll anfører selv i 2025, at den <em>"formegentlig"</em> er fravalgt af økonomiske årsager. Der ses ikke truffet nogen dokumenteret myndighedsafgørelse om at fravige vilkåret. Dokumentet indgår nu i klagesagen som bilag 20.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot open red"></div>
    <div class="tl-body">
      <span class="tl-tag">Igangværende</span>
      <p class="tl-title">Klagen indgives — Ankestyrelsen først</p>
      <p class="tl-text">GRG fremsender sin anmodning til <strong>Ankestyrelsens kommunale tilsyn</strong> om at tage stilling til, om kommunens sagsbehandling har været lovlig — manglende sagsoplysning, manglende dokumentation for vilkårsopfyldelse og manglende genoptagelse trods kommunens egne erkendelser. Anmodningen anfægter ikke VVM-tilladelsen selv, men spørger, om kommunen lovligt har kunnet anse bindende vilkår for opfyldt uden at kunne dokumentere det.</p>
      <p class="tl-text">Spørgsmålet er ikke et spørgsmål om god tone eller god service. Efter <a href="https://danskelove.dk/planloven/51">planlovens § 51</a> <em>påser</em> kommunalbestyrelsen, at <em>"vilkår fastsat i tilladelser, dispensationer m.v. overholdes"</em>, og den <em>skal</em> <em>"foranledige et ulovligt forhold lovliggjort, medmindre forholdet har underordnet betydning."</em> Det er en lovbestemt pligt — og den påhviler kommunen i begge dens roller her: som myndighed efter § 51, og som ejer af anlægget efter lovens § 63. En klage til <strong>Folketingets Ombudsmand</strong> over aktindsigtsforløbet forberedes. Et klagespor til <strong>klagenævnet</strong> ligger klar, men kan først aktiveres, hvis kommunen træffer en formel afgørelse om vilkårsopfyldelse — og skal da indgives inden fire uger. Spørgsmålet, der stadig venter svar, er simpelt: hvad er der reelt brugt 20 mio. skatteborger-kroner på?</p>
    </div>
  </li>

</ul>

<div class="timeline-footer">
  Denne tidslinje er tiltænkt som bilag 1 til Giber Ringvej Gruppens anmodning til Ankestyrelsens kommunale tilsyn. Anmodningen er endnu ikke indgivet, og både tidslinjen og anmodningen har status af kladde. Hvor der er anført citater, stammer de fra de dokumenter, der er linket i den enkelte post; de fulde kildedokumenter er vedlagt klagen som bilag. Tidslinjen anfægter ikke VVM-tilladelsens indhold eller gyldighed, men beskriver forløbet omkring dokumentationen for, om dens vilkår er opfyldt.<br><br>
  Giber Ringvej Gruppen repræsenterer beboere langs Giber Ringvej i Aarhus. Kontakt: jakob@aarhusworks.com
</div>

</div>
