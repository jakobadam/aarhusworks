// Counts the number of times a term is mentioned in the hearing content pages (only html, not the pdf).
//
// execute js on the page itself by copy-pasting it to
// https://deltag.aarhus.dk/hoering/forslag-til-stoejhandlingsplan-2024

const terms = [
    'Viby',
    'Giber',
    '(Gren.*vej|Skæring)',
    '(Djursland|Skødstrup|Løgten)',
    'Sta(u|v)trup',
    'Viborg',
    'Silkeborg',
    'Slet',
    'Tranbjerg',
    'Kolt',
    'Hasselager',
    'Randers',
    'Højbjerg',
    '(Herredsvej|herresvej)',
    'Lisbjerg',
    'Runevej',
    '(Motorvej Syd|Syd Motorvejen|Århus Syd)',
    'Tilst',
    'E45',
    'Blåhøjtoft.*',
    'Oddervej',
    'Nørre All',
    'Lystrup',
    'Ringgade',
    'Ormslevvej',
    'Hasle',
    'Bøgeskov',
]

const regexes = terms.map(t => new RegExp(t, 'i'))

const matches = (text) => {
    for(let i = 0; i < regexes.length; i++) {
        const r = regexes[i];
        const match = r.test(text);
        if(match) {
            return { term: terms[i], text: text };
        }
    }
    return null;
};
const ticketLinks = Array.from(document.querySelectorAll('.hearing-ticket'));

const stats = {};

// search for regex in page content and increment matched term count
const search = (ticketLink) => {
    const text = ticketLink.innerText;
    const matchInfo = matches(text);
    if(!matchInfo?.term) {
        console.log('no match', text);
    }
    const term = matchInfo?.term || 'andre';
    if (term) {
        if(stats[term] === undefined) {
            stats[term] = [];
        }
        stats[term].push(ticketLink.href);
    }
}

function doIt() {
    for (let i = 0; i < ticketLinks.length; i++) {
        search(ticketLinks[i]);
    }
    
    console.log(stats)

    const sortedStats = Object.entries(stats).sort((a, b) => b[1].length - a[1].length);

    sortedStats.forEach(([term, urls]) => {
        console.log(`${term} (${urls.length})`);
    });

    Object.entries(stats['andre']).forEach(link => console.log(link));
}

doIt();



