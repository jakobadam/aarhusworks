// execute js on the page itself by copy-pasting it to
// https://deltag.aarhus.dk/hoering/forslag-til-stoejhandlingsplan-2024

const terms = [
    'Viby',
    'Giber',
    'Gren.*vej',
    'Djursland',
    'Sta(u|v)trup',
    'Viborg',
    'Silkeborg',
    'Slet',
    'Tranbjerg',
    'Kolt',
    'Hasselager',
    'Randers',
    'Højbjerg',
    'Herredsvej',
    'Lisbjerg',
    'Runevej',
    'Motorvej Syd',
    'Tilst'
]

const regexes = terms.map(t => new RegExp(t, 'ig'))


const matches = (text) => {
    const matchIndex = regexes.findIndex(r => r.test(text));
    if (matchIndex !== -1) {
        return { term: terms[matchIndex], text: text };
    }
    return null;
};
const ticketLinks = Array.from(document.querySelectorAll('.hearing-ticket')).map(a => a.href);

const stats = {};

// search for regex in page content and increment matched term count
const search = async (url) => {
    
    const response = await fetch(url);
    const text = await response.text();
    const matchInfo = matches(text);
    const term = matchInfo?.term || 'andre';
    if (term) {
        if(stats[term] === undefined) {
            stats[term] = [];
        }
        stats[term].push(url)
    }
}

await Promise.all(ticketLinks.map(search));

console.log(stats)

const sortedStats = Object.entries(stats).sort((a, b) => b[1].length - a[1].length);

sortedStats.forEach(([term, urls]) => {
    console.log(`${term} (${urls.length})`);
});

Object.entries(stats['andre']).forEach(link => console.log(link));
