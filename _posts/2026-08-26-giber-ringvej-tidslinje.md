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

  /* Uden dette lægges padding og rammer oven i procentbredder,
     hvilket giver vandret overløb på smalle skærme. */
  .timeline-wrap,
  .timeline-wrap *,
  .timeline-wrap *::before,
  .timeline-wrap *::after {
    box-sizing: border-box;
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

  .timeline-deck p {
    margin: 0 0 0.75rem 0;
  }

  .timeline-deck p:last-child {
    margin-bottom: 0;
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

  .tl-tablewrap {
    overflow-x: auto;
    margin: 1rem 0 0.4rem 0;
  }

  .tl-table {
    border-collapse: collapse;
    width: 100%;
    min-width: 22rem;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.8rem;
    line-height: 1.4;
  }

  .tl-table th,
  .tl-table td {
    text-align: left;
    padding: 0.4rem 0.7rem 0.4rem 0;
    border-bottom: 1px solid #e5e5e5;
    vertical-align: top;
  }

  .tl-table th {
    font-size: 0.64rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    border-bottom: 2px solid #111;
  }

  .tl-table td.num,
  .tl-table th.num {
    text-align: right;
    white-space: nowrap;
    padding-right: 0;
  }

  .tl-table tr.sum td {
    font-weight: 700;
    color: #111;
    border-bottom: none;
    border-top: 2px solid #111;
  }

  .tl-table .nej { color: #c00; font-weight: 700; }

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

  /* --- Mobil --- */
  @media (max-width: 620px) {
    .timeline-wrap { padding: 0 0.9rem; }

    .timeline-headline { font-size: 1.85rem; }
    .timeline-deck { font-size: 1rem; padding: 0.8rem 0; margin-bottom: 1.8rem; }

    /* Tidslinjen: streg helt til venstre, dato som etiket over teksten */
    .tl::before { left: 5px; }

    .tl-item {
      flex-wrap: wrap;
      gap: 0 0.8rem;
      align-items: flex-start;
    }

    .tl-dot {
      order: 1;
      margin-top: 0.75rem;
    }

    .tl-date {
      order: 2;
      flex: 1 1 auto;
      text-align: left;
      padding-top: 0.55rem;
      display: flex;
      align-items: baseline;
      gap: 0.45rem;
    }

    .tl-year { font-size: 1rem; }
    .tl-month { margin-top: 0; }

    .tl-body {
      order: 3;
      flex: 0 0 100%;
      padding: 0.35rem 0 1.4rem 1.55rem;
    }

    .tl-title { font-size: 1rem; }
    .tl-text { font-size: 0.88rem; }

    .tl-divider { margin-left: 1.55rem; }

    .tl-fig { margin: 0.9rem 0 0.2rem 0; }
  }

  /* Meget smalle skærme */
  @media (max-width: 380px) {
    .timeline-headline { font-size: 1.6rem; }
    .tl-body { padding-left: 1.3rem; }
    .tl-divider { margin-left: 1.3rem; }
  }

  /* --- Fund-boks --- */

  /* Vilkaarsnummeret er en genvej til selve tilladelsesteksten */
  .track-nr a {
    color: inherit;
    text-decoration: none;
    border-bottom: 1px dotted #bbb;
  }

  .track-nr a:hover { color: #c00; border-bottom-color: #c00; }

  .kladde-note {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.76rem;
    line-height: 1.5;
    font-style: italic;
    color: #888;
    margin: 0 0 2.4rem 0;
  }

  /* --- Tidslinjens akse ---
     Prikken er tredje flex-element efter datokolonnen, saa aksen ligger paa
     datobredde + gap + halv prik. Den var haardkodet til 5.8rem og ramte
     derfor ca. 27 px til venstre for prikkerne. Nu udregnes den af de samme
     tal, som layoutet bruger. */
  .tl {
    --tl-date-w: 5.6rem;
    --tl-gap: 1.6rem;
    --tl-dot-size: 12px;
  }

  .tl::before {
    left: calc(var(--tl-date-w) + var(--tl-gap) + var(--tl-dot-size) / 2 - 1px);
  }

  .tl-divider {
    margin-left: calc(var(--tl-date-w) + var(--tl-gap) + var(--tl-dot-size) + var(--tl-gap));
  }

  /* --- Vaegtning: tunge poster mod lette ---
     Alle prikker har samme diameter, saa broedteksten flugter paa tvaers af
     posterne og alle centre rammer samme akse. Vaegten ligger i fyld og ring. */
  .tl-item--key .tl-title { font-size: 1.3rem; line-height: 1.2; }
  .tl-item--key .tl-dot { box-shadow: 0 0 0 4px #c00; }

  .tl-item--slim .tl-body { padding-top: 1rem; padding-bottom: 1.1rem; }
  .tl-item--slim .tl-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.25rem;
  }
  .tl-item--slim .tl-text { font-size: 0.86rem; }
  .tl-item--slim .tl-dot {
    background: #fff;
    box-shadow: 0 0 0 2px #999;
  }

  @media (max-width: 620px) {
    .tl-item--key .tl-title { font-size: 1.1rem; }
    /* Paa mobil er prikken foerste element, saa aksen ligger i dens midte */
    .tl::before { left: calc(var(--tl-dot-size) / 2 - 1px); }
    /* Blokkene ovenfor staar uden for media-forespoergslen og ville ellers
       overskrive mobilreglerne, fordi de kommer senere i kaskaden. */
    .tl-divider { margin-left: 1.55rem; }
    .tl-item--slim .tl-body { padding-top: 0.35rem; padding-bottom: 1.1rem; }
  }

  @media (max-width: 380px) {
    .tl-divider { margin-left: 1.3rem; }
  }

  .ovrige {
    border-top: 3px solid #111;
    padding: 1.1rem 0 0 0;
    margin: 2.6rem 0 0 0;
  }

  .ovrige-title {
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #c00;
    margin: 0 0 0.5rem 0;
  }

  .ovrige-intro {
    font-size: 0.9rem;
    color: #555;
    margin: 0 0 1.1rem 0;
  }

  .ovrige ul { list-style: none; margin: 0; padding: 0; }

  .ovrige li {
    font-size: 0.92rem;
    line-height: 1.5;
    padding: 0.45rem 0;
    border-bottom: 1px solid #e6e6e6;
  }

  .ovrige li:last-child { border-bottom: 0; }

  .ovrige .ovr-dato {
    display: inline-block;
    min-width: 5.4rem;
    font-family: 'Arial Narrow', Arial, sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #888;
  }

  @media (max-width: 640px) {
    .ovrige .ovr-dato { display: block; min-width: 0; margin-bottom: 0.1rem; }
  }

  .ovrige-slut {
    font-size: 0.95rem;
    line-height: 1.55;
    margin: 1.4rem 0 0 0;
    padding-top: 1.1rem;
    border-top: 3px solid #c00;
  }
</style>

<div class="timeline-wrap">

<p class="timeline-kicker">Snart otte år efter VVM-tilladelsen</p>
<h1 class="timeline-headline">Giber Ringvej: Ingen træer. Ingen støjskærme. Intet facade&shy;tilskud — trods byrådets beslut&shy;ninger.</h1>
<div class="timeline-deck">
  <p>Aarhus Kommune fik i 2018 en VVM-tilladelse til Giber Ringvej på tre bindende vilkår: slørende beplantning, støjdæmpende vejbelægning og supplerende støjdæmpning inden for <em>ca. 20 mio. kr.</em> Kommunen fastholder, at alle tre er opfyldt. Tilbage står én støjskærm — den, kommunen skyldte efter et andet vilkår — og en asfalt, kommunen ikke kan oplyse dæmpningen af.</p>
  <p>Grundlaget for de 20 mio. kr. kom først frem i 2026. Beløbet er summen af fem prissatte tiltag på præcis de fem steder, vilkåret nævner: tre støjskærme til 16,7 mio. kr., et facadetilskud og en afklaring ved Beder Landevej. Byrådet vedtog dem i 2016 mod forvaltningens indstilling og finansierede dem i 2020. Skærmene er aldrig bygget.</p>
</div>

<p class="kladde-note">Kladde. Anmodningen til Ankestyrelsen er endnu ikke indgivet. Alle citater stammer fra de dokumenter, der er linket i den enkelte post.</p>

<div class="tracks">

  <div class="track track--beplantning">
    <span class="track-nr"><a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=2">Vilkår 2 &rsaquo;</a></span>
    <span class="track-name">Slørende beplantning</span>
    <p class="track-req">Anlægget skal tilpasses landskabet <em>"i henhold til anvisningerne i VVM redegørelsen"</em> — og de foreskriver beplantning ved tæt bebyggelse.</p>
    <p class="track-status"><strong>Status:</strong> Ikke etableret ved Mårslet. Ingen dokumenteret afgørelse om at fravige vilkåret.</p>
  </div>

  <div class="track track--belaegning">
    <span class="track-nr"><a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=2">Vilkår 5 &rsaquo;</a></span>
    <span class="track-name">Støjdæmpende vejbelægning</span>
    <p class="track-req">Hele vejanlægget skal udformes med støjdæmpende vejbelægning. Projektet forudsatte ifølge Rambøll en SRS-belægning.</p>
    <p class="track-status"><strong>Status:</strong> Der er udlagt KVS. Hverken referencebelægning, type eller dokumenteret støjreduktion er oplyst.</p>
  </div>

  <div class="track track--pulje">
    <span class="track-nr"><a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=3">Vilkår 7 &rsaquo;</a></span>
    <span class="track-name">Pulje på ca. 20 mio. kr.</span>
    <p class="track-req">Der skal <em>suppleres</em> med øget støjdæmpning ved Tranbjerg, Mårslet, Kolt, forlængelsen til Beder Landevej og i det åbne land.</p>
    <p class="track-status"><strong>Status:</strong> Ingen af de tre støjskærme, rammen blev afsat til, er opført. Intet særskilt regnskab.</p>
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
      <p class="tl-title">Borgerne ser et projekt, hvor træer skjuler vejen</p>
      <p class="tl-text"><a href="/assets/giber-ringvej/2013-vvm.pdf#page=77">VVM-redegørelsen</a> i høring: <em>"Hvor der er nærliggende tæt bebyggelse ønskes vejanlægget sløret med en beplantning"</em> (s. 77). Vilkår 2 gør fire år senere anvisningen bindende.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2026-vvm-figur44-s85-visualisering-tandervej-maarslet.png" alt="Terrænvisualisering fra VVM-redegørelsen: udsigten fra Mårslet langs Tandervej mod syd, med træbeplantning langs den kommende vej.">
        <figcaption>Figur 44: udsigten fra Mårslet mod syd, <em>"med beplantning langs Bering-Beder vejen, som vil sløre bilerne i landskabet."</em> Det var dette projekt, borgerne tog stilling til. Træerne står der ikke.</figcaption>
      </figure>
      <p class="tl-text">Redegørelsen viser krydsningen af Giber Å fra samme standpunkt to gange — først som vejen vil fremstå <a href="/assets/giber-ringvej/2013-vvm.pdf#page=88">umiddelbart efter etableringen</a>, og dernæst med beplantning på skråningsanlæggene. Det er den anden version, redegørelsen selv sætter navn på:</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2026-vvm-figur50-s89-beplantning-som-afvaergeforanstaltning-maarslet-og-testrup.png" alt="Terrænvisualisering fra VVM-redegørelsen af krydsningen ved Giber Å, hvor beplantning på skråningsanlæggene skjuler vejen. Billedet er påført teksten &quot;Beplantning som afværgeforanstaltning&quot;.">
        <figcaption>Figur 50 (s. 89): <em>"Beplantning på skråningsanlæggene slører den visuelle støj fra bilerne."</em> Kommunen har selv påført billedet ordene <strong>"Beplantning som afværgeforanstaltning"</strong> — den term, VVM-tilladelsen bruger om det, tilladelsen er meddelt <em>på grundlag af</em>. Otte år senere er kommunens standpunkt, at beplantningen <em>"ikke [var] forudsat etableret"</em>.</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item tl-item--key">
    <div class="tl-date">
      <span class="tl-year">2016</span>
      <span class="tl-month">Sep</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Sagens omdrejningspunkt</span>
      <p class="tl-title">De 20 millioner var fem prissatte tiltag — tre af dem støjskærme</p>
      <p class="tl-text">Teknisk Udvalg indstiller den 5. september, og byrådet vedtager den 14. september, at der afsættes <em>ca. 20 mio. kr.</em> til øget støjdæmpning. <a href="/assets/giber-ringvej/2016-udvalgs-erklaering.pdf#page=1">Ordlyden</a> er, at den skitserede afskærmning <em>"<strong>fastholdes og suppleres med</strong>"</em> mere ved Mårslet, Tranbjerg, Kolt og Beder Landevej. Puljen skal altså lægges <em>oven i</em> det, projektet allerede indeholdt.</p>
      <p class="tl-text">Grundlaget fik borgerne først i 2026. Forvaltningen havde forelagt udvalget <a href="/assets/giber-ringvej/2016-09-01-tu-svar.pdf#page=4">et skema</a> med fem prissatte tiltag — på præcis de fem steder, vilkår 7 to år senere navngiver. Summen er ca. 21,4 mio. kr.</p>
      <p class="tl-text"><strong>Her er de fem poster — og hvad der siden er blevet af dem:</strong></p>
      <div class="tl-tablewrap">
        <table class="tl-table">
          <thead>
            <tr><th>Foranstaltning (<a href="/assets/giber-ringvej/2016-08-cowi-trafikstoej.pdf">COWI, aug. 2016</a>)</th><th class="num">Pris</th><th>Gennemført</th></tr>
          </thead>
          <tbody>
            <tr><td>Kolt — 4 m støjskærm, ca. 1.200 m</td><td class="num">8,2 mio. kr.</td><td><span class="nej">Nej</span></td></tr>
            <tr><td>Tranbjerg — forøgelse af skærm fra 4 til 6 m</td><td class="num">5,4 mio. kr.</td><td><span class="nej">Nej</span> — skærmen står i de 4 m, vilkår 6 kræver</td></tr>
            <tr><td>Mårslet — 4 m støjskærm, 450 m</td><td class="num">3,1 mio. kr.</td><td><span class="nej">Nej</span></td></tr>
            <tr><td>Det åbne land — tilskud til facadedæmpning ved over 58 dB</td><td class="num">op til 2,7 mio. kr.</td><td><span class="nej">Optræder ikke</span> i kommunens egen opgørelse</td></tr>
            <tr><td>Beder Landevej — afklares i detailprojekteringen</td><td class="num">2,0–2,2 mio. kr.</td><td>Ikke udskilt</td></tr>
            <tr class="sum"><td>I alt</td><td class="num">ca. 21,4 mio. kr.</td><td>—</td></tr>
          </tbody>
        </table>
      </div>
      <p class="tl-text">Projektets eneste støjskærm står langs Landevejen i Tranbjerg — den, vilkår 5 og 6 kræver uafhængigt af puljen. Den tælles alligevel med som forbrug af rammen.</p>
      <p class="tl-text"><strong>Forvaltningen frarådede de tre skærme.</strong> Teknik og Miljø anbefalede i <a href="/assets/giber-ringvej/2016-09-01-tu-svar.pdf#page=4">samme notat</a>, at der <em>"<strong>ikke</strong>"</em> blev etableret støjdæmpning ved Kolt, Mårslet og Tranbjerg, fordi <em>"de gældende støjgrænser kan overholdes"</em>. Fire dage senere vedtog Teknisk Udvalg det modsatte. Det eneste tiltag, forvaltningen <em>selv</em> anbefalede, var facadetilskuddet — og det optræder heller ikke i kommunens opgørelse over, hvad puljen er brugt til.</p>
      <p class="tl-text">Det afgør sagens centrale strid. Kommunen afviser i dag mere støjdæmpning med, at grænseværdierne er overholdt. Men det var forudsætningen for beslutningen, ikke en indvending mod den: pengene blev netop afsat til det, der lå <em>ud over</em> grænsen.</p>
    </div>
  </li>

  <li class="tl-item tl-item--key">
    <div class="tl-date">
      <span class="tl-year">2018</span>
      <span class="tl-month">Okt</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-tag">Juridisk grundlag</span>
      <p class="tl-title">VVM-tilladelsen gør det bindende</p>
      <p class="tl-text"><a href="/assets/giber-ringvej/2018-vvm-tilladelse.pdf#page=2">Tilladelsen</a> har 18 vilkår. <strong>Vilkår 2</strong> gør VVM-redegørelsens anvisninger — herunder beplantningen — bindende. <strong>Vilkår 5 og 6</strong> kræver støjdæmpende belægning og afskærmning ved Tranbjerg og langs Landevejen. <strong>Vilkår 7</strong> kræver, at der <em>suppleres</em> med øget støjdæmpning fem steder inden for rammen — og henviser tilbage til beslutningen fra 2016, ikke til noget senere projektdokument.</p>
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
      <p class="tl-title">Rådgiverens egen plan udpeger stedet, hvor træerne mangler</p>
      <p class="tl-text">Rambølls interne <a href="/assets/giber-ringvej/2019-landsskabstrategi.pdf">Landskabsstrategi</a> omsætter vilkår 2 til konkrete tiltag. Ved Mårslet, vest for Tandervej, står punktet <em>"Visuel støjskærmning (beplantning) nordside af vej"</em>. Dokumentet udleveres først syv år senere.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2019-landskabsstrategi-st9200-9660-vest-for-tandervej.png" alt="Udsnit af Landskabsstrategiens tiltagsliste for strækningen St. 9.200-9.660 &quot;Vest for Tandervej&quot;. Blandt de opregnede tiltag står &quot;Visuel støjskærmning (beplantning) nordside af vej&quot;.">
        <figcaption>Om netop denne strækning erkender Rambøll syv år senere, at beplantning er <a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-08-notat-redegoerelse-for-beplantning.pdf#page=4"><em>"formegentlig fravalgt af økonomiske årsager"</em></a>.</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item tl-item--slim">
    <div class="tl-date">
      <span class="tl-year">2019–20</span>
      <span class="tl-month">Aug–Mar</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <p class="tl-title">Byrådet betaler for skærmene — og så holder bogføringen op</p>
      <p class="tl-text">Byrådet godkender <a href="/assets/giber-ringvej/2019-08-06-projektgodkendelse.pdf#page=5">projektet</a> i august 2019 og <a href="/assets/giber-ringvej/2025-04-02-redegoerelse-3-mail.pdf#page=1">bevilger anlægget</a> den 11. marts 2020, hvor <em>"puljen på 20 mio. kr. indgår i Bilag 6: Anlægsoverslag"</em>. Pengene er dermed både besluttet og finansieret. Derefter, skriver <a href="/assets/giber-ringvej/2026-03-ramboell-kommentering-af-faktaark.pdf#page=3">rådgiveren</a>, <em>"føres der ikke separat regnskab med midler anvendt til støjtiltag"</em>. Alt, kommunen siden fremlægger, er rekonstruktion — ikke regnskab.</p>
    </div>
  </li>

  <li class="tl-item tl-item--key">
    <div class="tl-date">
      <span class="tl-year">2023</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Redegørelse 1</span>
      <p class="tl-title">"16 støjvolde for 17,28 mio. kr." — og én eneste støjskærm</p>
      <p class="tl-text"><a href="/assets/giber-ringvej/2023-08-Ramboll-redegoerelse.pdf#page=1">Rambølls redegørelse</a> henfører 17,28 mio. kr. til puljen — vilkår 7 dermed opfyldt. Men opgørelsen rummer en vejsænkning, rådgiveren selv senere kalder en <em>"tracérings-mæssig konsekvens"</em>, en skærm hjemlet i vilkår 5 og 6, samt tilkørselsveje og jorddeponier. De 16 volde prissættes under ét til 18,5 mio. kr. uden mængdeopgørelse.</p>
      <p class="tl-text">Opgørelsen er samtidig beviset for, hvad der <em>ikke</em> blev bygget. <a href="/assets/giber-ringvej/2023-08-Ramboll-redegoerelse.pdf#page=4">Listen på side 4</a> opregner alt, kommunen henfører til støj — og indeholder <strong>én støjskærm:</strong> <em>"Støjskærm langs Landevejen — ca. 5.200.000,00 kr."</em> De tre skærme fra 2016 optræder ikke. <a href="/2023/08/23/stoej-langs-giber-ringvej--et-modsvar-til-kommunen.html">GRG svarer samme måned</a>.</p>
    </div>
  </li>

  <li class="tl-item">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Jan–Feb</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <span class="tl-tag">Redegørelse 2</span>
      <p class="tl-title">"Misvisende" — men konklusionen står fast</p>
      <p class="tl-text"><a href="/assets/giber-ringvej/2025-01-mtm-redegoerelse-2.pdf#page=1">Redegørelse 2</a> anerkender, at rapporten <em>"kan give et misvisende billede af økonomi anvendt til støjdæmpning"</em>, at der ikke har været økonomistyring med henblik på at opgøre støjudgifterne, og at det var <em>"misvisende, at det fremgik, at der var etableret 16 støjvolde, da ikke alle jorddepoterne er anlagt som deciderede støjvolde"</em>. Opgørelsen er efter forvaltningens egen beskrivelse <em>"alene et udtryk for et estimat"</em>. Konklusionen er uændret: vilkårene er overholdt.</p>
      <p class="tl-text">GRG svarer med <a href="/vejst%C3%B8j/2025/02/25/de-19-millioner-der-forsvandt.html"><em>De 19 millioner der forsvandt</em></a>: jordvolde af overskudsjord kan ifølge <a href="/assets/vejstoej-forslag-2024/trafikstoej-kraever-handling-2020.pdf#page=46">branchens egen hvidbog</a> — medforfattet af Rambøll — etableres for <em>"meget små eller ingen omkostninger"</em>, og <a href="/assets/giber-ringvej/2025-01-29-vejdirektoratet-stavtrup-jordvold-oekonomi.txt">Vejdirektoratet</a> siger det samme. <a href="https://dinavis.dk/samfund/ECE18005991/borgere-klager-over-trafikstoej-fra-giber-ringvej-hvad-blev-der-af-de-20-mio-kr">Din Avis</a> og <a href="https://stiften.dk/debat/vi-undrer-os-her-ved-giber-ringvej-19-millioner-kroner-er-aabenbart-forsvundet">Stiften</a> omtaler sagen. Borgmesteren beder om en ny redegørelse.</p>
    </div>
  </li>

  <li class="tl-item tl-item--slim">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Maj</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--pulje">Spor · Puljen</span>
      <p class="tl-title">Rådgiveren havde hele tiden givet GRG ret</p>
      <p class="tl-text">Efter gentagne enslydende aktindsigtsbegæringer dukker <a href="/assets/giber-ringvej/aktindsigt-20-mio-mails/2024-11-04-vedhaeftning-hoeringssvar-2-med-besvarelse-fra-ramboell.pdf">Rambølls annoterede besvarelse</a> fra november 2024 op. Rådgiveren tiltræder heri skriftligt, at fire af de påberåbte tiltag ikke kan medregnes som støjtiltag — blandt andet: <em>"Det er korrekt at letbanevolden ikke er et støjtiltag."</em> Ingen af forbeholdene stod i det svar, kommunen sendte.</p>
    </div>
  </li>

  <li class="tl-item tl-item--key">
    <div class="tl-date">
      <span class="tl-year">2025</span>
      <span class="tl-month">Aug</span>
    </div>
    <div class="tl-dot red"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <p class="tl-title">Forvaltningen spørger sin rådgiver, om træerne var et krav</p>
      <p class="tl-text">Med et kort indsat i mailen spørger <a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-08-07-mail-bestilling-af-redegoerelse-for-beplantning.pdf">bestillingen</a>: <em>"Men er det bare uforpligtende eksempler i VVM'en eller er det forudsætninger for projektet?"</em> Forvaltningen havde altså i 2025 ikke selv taget stilling til det spørgsmål, hele sagen handler om.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2025-08-07-mtm-bestilling-roed-markering-vest-for-tandervej.png" alt="Luftfoto med rød markering langs nordsiden af Giber Ringvej umiddelbart vest for Tandervej ved Mårslet.">
        <figcaption>Forvaltningens eget kortudsnit. Det røde område er <strong>samme strækning</strong>, som Landskabsstrategien seks år tidligere udpegede til afskærmende beplantning.</figcaption>
      </figure>
      <p class="tl-text"><a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-08-notat-redegoerelse-for-beplantning.pdf#page=4">Svaret</a> peger på to nabostrækninger. <strong>Vest for Tandervej</strong> — netop det røde område — er beplantningen <em>"formegentlig fravalgt af <strong>økonomiske årsager</strong>"</em>. <strong>Øst for Tandervej</strong> begrundes fravalget med en borgerdialog, der foregik <em>"uden om Rambølls involvering"</em>. Ingen af delene er journaliseret — der findes ingen afgørelse om at fravige vilkåret.</p>
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
      <span class="tl-tag">Vilkår 5</span>
      <p class="tl-title">Den støjdæmpende asfalt, der ikke dæmper støj</p>
      <p class="tl-text">Vilkår 5 kræver støjdæmpende vejbelægning på hele anlægget, og projektet forudsatte ifølge Rambøll <em>"den typisk valgte belægning til dette formål (...) en SRS"</em>. Der blev i stedet udlagt KVS — klimavenligt slidlag. GRG rejser i <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-1-vvm-giber-ringvej.pdf">afklaringsnotat 1</a> tre spørgsmål: hvilken referencebelægning er lagt til grund, hvilken KVS-type er udlagt, og hvilken dokumenteret støjreduktion kan lægges til grund? Ingen af dem er besvaret.</p>
      <figure class="tl-fig">
        <img src="/assets/giber-ringvej/klage/2019-vejdirektoratet-kvs-figur1-stoejtrendlinjer-kvs-sma8-sma11-srs.png" alt="Vejdirektoratets graf over støjudviklingen for asfalttyperne SMA8, SMA11, SRS og KVS som funktion af belægningens alder. Ved nyudlægning ligger SRS lavest, dernæst SMA8, så KVS og øverst SMA11.">
        <figcaption><strong>Vejdirektoratets egen figur.</strong> Ved nyudlægning er KVS (gul) den <em>højeste</em> af de tre alternativer: 98,0 dB mod SMA8's 96,9 og SRS'ens 96,6. Over levetiden følges KVS og standardbelægningen SMA8 (grøn) inden for ca. 1 dB. Den reduktion på ca. 2 dB, KVS fremhæves for, er målt mod den grovere SMA11 (blå) — ikke mod SMA8, som i dag udgør omkring 70 % af statsvejnettet. Kilde: <a href="/assets/giber-ringvej/2019-08-vejdirektoratet-kvs-asfalt.pdf#page=4">Vejdirektoratet, august 2019, figur 1</a>.</figcaption>
      </figure>
    </div>
  </li>

  <li class="tl-item tl-item--key">
    <div class="tl-date">
      <span class="tl-year">2026</span>
      <span class="tl-month">Jun</span>
    </div>
    <div class="tl-dot"></div>
    <div class="tl-body">
      <span class="tl-spor tl-spor--beplantning">Spor · Beplantning</span>
      <p class="tl-title">Hullet, hvor kommunen selv har målt højest</p>
      <p class="tl-text">Forvaltningens beplantningsforslag dækker ikke den strækning ved Mårslet, som kommunens egen <a href="/assets/giber-ringvej/2019-landsskabstrategi.pdf">landskabsstrategi</a> udpeger til <em>"visuel støjskærmning (beplantning) nordside af vej"</em>. Kommunen beskriver den selv som strækningen <em>"mellem rundkørsel og Mustrupvej"</em> — og dér ligger Damgårdstoften 65, hvor <a href="/assets/mtm-modsvar/2023-08-VM-accoustics-m%C3%A5lt-trafikst%C3%B8j.pdf#page=5">kommunens egen måling</a> gav den højeste af ti værdier: 57,4 dB. Rådmanden bad i april forvaltningen undersøge hullet. Den 12. juni <a href="/assets/giber-ringvej/2026-moede-opfoelgning-aktindsigt-landsskabstrategi.pdf">svarede</a> forvaltningen: <em>"Vi vender tilbage snarest muligt."</em> Der er ikke kommet svar.</p>
    </div>
  </li>

  </ul>

<div class="ovrige">
  <p class="ovrige-title">Øvrige poster i forløbet</p>
  <p class="ovrige-intro">Tidslinjen ovenfor viser sagens elleve hovedpunkter. Nedenfor står de øvrige begivenheder med kilde, i samme rækkefølge.</p>
  <ul>
    <li><span class="ovr-dato">Maj 2019</span> Mårslet får en jordvold på én meter &middot; <a href="/assets/giber-ringvej/2019-05-27-landzonetilladelse-stoejvold-nymarksvej.pdf#page=2">landzonetilladelse</a></li>
    <li><span class="ovr-dato">Jan 2022</span> Kommunen afgør selv, at en af voldene ikke er et støjtiltag &middot; <a href="/assets/giber-ringvej/2022-01-26-screeningafgoerelse-jordvold-koelsmosevej.pdf#page=3">Screeningsafgørelsen</a></li>
    <li><span class="ovr-dato">Efterår 2022</span> Giber Ringvej åbner for trafik &middot; <a href="/assets/giber-ringvej/2026-03-ramboell-kommentering-af-faktaark.pdf#page=3">ifølge Rambøll</a> &middot; <a href="/assets/giber-ringvej/stoejhandlingsplan-hoeringsbidrag.pdf">høringssvar</a></li>
    <li><span class="ovr-dato">Mar 2023</span> De to spørgsmål, der stadig venter svar &middot; <a href="/assets/giber-ringvej/2023-03-20-grg-bilag-til-teknisk-udvalg.pdf">bilag</a></li>
    <li><span class="ovr-dato">Maj 2023</span> Svarene pilles ud af notatet, før udvalget ser det &middot; <a href="/assets/giber-ringvej/aktindsigt-20-mio-mails/2023-05-09-mail-re-stoejmaaler-ved-giber-ringvej.pdf">aktindsigten</a></li>
    <li><span class="ovr-dato">Nov 2023</span> "Ikke afregnet" — og kommunalfuldmagten som spærring &middot; <a href="/assets/giber-ringvej/2023-11-22-mtm-svar-pulje-og-kommunalfuldmagt.pdf">oplyser</a> &middot; <a href="/assets/giber-ringvej/2023-04-13-mtm-juridisk-notat-stoejafskaermning.pdf#page=3">notatet</a></li>
    <li><span class="ovr-dato">Sep 2024</span> Udvalgsformanden: "Vi skal have et faktatjek" &middot; <a href="/assets/giber-ringvej/aktindsigt-20-mio-mails/2023-05-09-mail-re-stoejmaaler-ved-giber-ringvej.pdf">internt</a></li>
    <li><span class="ovr-dato">Apr 2025</span> I retten forklares den samme vold anderledes &middot; <a href="/assets/giber-ringvej/2025-04-07-dom-retten-i-aarhus-bs-38128-2021-arh.pdf#page=57">dommen, s. 57</a></li>
    <li><span class="ovr-dato">Apr–Maj 2025</span> "Byrådet afgjorde det i 2019" — sagen lukket &middot; <a href="/assets/giber-ringvej/2025-04-02-redegoerelse-3-mail.pdf#page=1">Redegørelse 3</a> &middot; <a href="/assets/giber-ringvej/2025-05-faktaark-pulje-til-oeget-stoejdaempning-redegoerelse-3.pdf">faktaark</a></li>
    <li><span class="ovr-dato">Sep 2025</span> Prisen på de manglende træer: ca. 100.000 kr. &middot; <a href="/assets/giber-ringvej/aktindsigt-beplantning-afslag-nr-3/2025-09-26-mail-vs-redegoerelse-for-beplantning-prisoverslag.pdf">prissættes</a></li>
    <li><span class="ovr-dato">Jun–Feb 2025–26</span> Ni måneders venten og tre rykkere &middot; <a href="/assets/giber-ringvej/2025-2026-mailtraad-med-mtm-rykkere-for-svar-paa-faktaark.pdf">mailtråden</a></li>
    <li><span class="ovr-dato">Feb 2026</span> Borgmesteren afviser at genoptage sagen &middot; <a href="/assets/giber-ringvej/2026-02-borgmester-opfoelgning.pdf#page=1">fastholder</a></li>
    <li><span class="ovr-dato">Mar 2026</span> Rammen omfortolkes til "blot en omtrentlig angivelse" &middot; <a href="/assets/giber-ringvej/2026-03-ramboell-kommentering-af-faktaark.pdf#page=3">notatet</a></li>
    <li><span class="ovr-dato">Apr 2026</span> "Vi er juridisk uenige" &middot; <a href="/assets/giber-ringvej/2026-04-afklaringsnotat-2-20-mio-giber-ringvej.pdf">afklaringsnotater</a> &middot; <a href="/assets/giber-ringvej/2026-04-referat-GRG-og-MTM.txt">referatet</a></li>
  </ul>
  <p class="ovrige-slut"><strong>Hvor sagen står nu.</strong> Aarhus Kommune har to gange — i februar og april 2026 — afvist at genoptage sagen. Giber Ringvej Gruppen forbereder en anmodning til Ankestyrelsens kommunale tilsyn om at rejse en tilsynssag efter planlovens § 51.</p>
</div>


<div class="timeline-footer">
  Bilag 1 til Giber Ringvej Gruppens anmodning til Ankestyrelsens kommunale tilsyn. Anmodningen er endnu ikke indgivet. Citater stammer fra de dokumenter, der er linket i den enkelte post; de fulde kildedokumenter er vedlagt klagen som bilag. Tidslinjen anfægter ikke VVM-tilladelsens gyldighed, men beskriver forløbet omkring dokumentationen for, om dens vilkår er opfyldt.<br><br>
  Giber Ringvej Gruppen repræsenterer beboere langs Giber Ringvej i Aarhus. Kontakt: jakob@aarhusworks.com
</div>

</div>
