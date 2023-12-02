from bs4 import BeautifulSoup

html = '''
        <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/2MRlh">Joe Biden and Narendra Modi cement ties over defence and tech at New Delhi meeting | Financial Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/MaLwt">At G20, Biden Looks to Fill a Hole Left by Putin and Xi - The New York Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/kMcBG">Joe Biden pushes for bigger World Bank to combat China&rsquo;s rising influence | Financial Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://politico.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.politico.com/news/2023/09/07/absence-presence-dominance-g20-00114544">Who to watch, and why, at the G20 amid Xi and Putin's absence - POLITICO</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://nypost.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://nypost.com/2023/09/07/inside-track-on-kim-jong-uns-personal-train-service/">Inside track on Kim Jong Un's personal train service</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/M3c0g">G20: India or Bharat? A dinner invite sparks speculation as Modi&rsquo;s ministers push to rebrand the country | AP News</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/fCBBk#selection-3294.1-3302.1">Analysis: Xi reprimanded by elders at Beidaihe over direction of nation - Nikkei Asia</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/D8zMX#selection-1733.0-1737.123">Stage set for a disagreeable ASEAN summit in Jakarta - Asia Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/O9Vc4">U.S.-China rivalry dominates ASEAN talks as summits wrap up - The Japan Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/aQ7X4">ASEAN Snub: Biden Skips Key Summit, Angering Officials In Southeast Asia</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/dTrG2">In Southeast Asia, Kamala Harris is at the center of White House efforts to counterbalance China | International | EL PA&Iacute;S English</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/QVEDs">Ukraine War Fallout: Putin Loses Ground in South Caucasus</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://meduza.io&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://meduza.io/en/feature/2023/09/07/an-experienced-negotiator-and-a-proud-crimean-tatar">An experienced negotiator and a proud Crimean Tatar What the appointment of Ukraine&rsquo;s new defense minister says about Kyiv&rsquo;s evolving war strategy &mdash; Meduza</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://al-monitor.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.al-monitor.com/originals/2023/09/us-presses-uae-over-dual-use-goods-fueling-russias-war">US presses UAE over dual-use goods fueling Russia's war - Al-Monitor: Independent, trusted coverage of the Middle East</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://al-monitor.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.al-monitor.com/originals/2023/09/us-denies-it-had-blocked-ai-chip-sales-some-middle-eastern-countries">US denies it had 'blocked' AI chip sales to some Middle Eastern countries - Al-Monitor: Independent, trusted coverage of the Middle East</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://al-monitor.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.al-monitor.com/originals/2023/09/netanyahu-calls-zelenskyy-ukraine-israel-relations-take-new-dive">Netanyahu calls Zelenskyy as Ukraine-Israel relations take new dive - Al-Monitor: Independent, trusted coverage of the Middle East</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://politico.eu&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.politico.eu/article/elon-musk-ukraine-starlink-russia-crimea-war-drone-submarine-attack-sabotage/">Elon Musk sabotaged Ukrainian attack on Russian fleet in Crimea by turning off Starlink, new book says &ndash; POLITICO</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://twitter.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://twitter.com/elonmusk/status/1699917639043404146?t=QvIThCrnPNh6oaLwwgn4mw&amp;s=19">(2) Elon Musk on X: &quot;@MarioNawfal There was an emergency request from government authorities to activate Starlink all the way to Sevastopol. The obvious intent being to sink most of the Russian fleet at anchor. If I had agreed to their request, then SpaceX would be explicitly complicit in a major act of war and&hellip;&quot; / X</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://overtdefense.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.overtdefense.com/2023/09/06/breaking-uk-selects-new-assault-rifle/">BREAKING: UK Selects New Assault Rifle - Overt Defense</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://soldiersystems.net&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://soldiersystems.net/wp-content/uploads/2023/09/img_5275.jpg">img_5275.jpg (1259&times;1492)</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://ar15.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.ar15.com/media/mediaFiles/474441/hunter-posters-copy-2945577.jpg">hunter-posters-copy-2945577.jpg (1200&times;844)</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://navalnews.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.navalnews.com/naval-news/2023/09/north-koreas-new-submarine-carries-10-nuclear-missiles/">North Korea's New Submarine Carries 10 Nuclear Missiles - Naval News</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/0pmD8">China seeks to prop up currency after renminbi hits 16-year low | Financial Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://pcmag.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.pcmag.com/news/what-us-sanctions-huawei-mate-60-pro-launches-with-korean-memory-chip">What US Sanctions? Huawei Mate 60 Pro Launches With Korean Memory Chip | PCMag</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/Vk6sS">US to investigate chips used in Huawei&rsquo;s &lsquo;Made in China&rsquo; smartphone | Financial Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/MN7rx">China Bans iPhone Use for Government Officials at Work - WSJ</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://axios.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.axios.com/2023/09/07/saudi-india-uae-us-railway-deal-g20-middle-east">U.S., Saudi, India, UAE hope to ink railway deal to connect Middle East at G20</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://axios.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.axios.com/2023/09/06/biden-saudi-mega-deal-israel-trump">Trump privately urged to support Biden's Saudi-Israel peace deal</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/i2Sgs">Marion Mar&eacute;chal to lead Eric Zemmour's party in European elections</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://archive.ph&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://archive.ph/zsOEk">After Prigozhin&rsquo;s Death, a High-Stakes Scramble for His Empire - The New York Times</a>
      </div>
            <div class="tab">
        <img class="favIconImg" src="https://t2.gstatic.com/faviconV2?client=SOCIAL&amp;type=FAVICON&amp;fallback_opts=TYPE,SIZE,URL&amp;url=https://thedailybeast.com&amp;size=32">
        <a class="tabLink" rel="ugc" href="https://www.thedailybeast.com/yevgeny-prigozhins-men-poached-in-wagner-hiring-spree-linked-to-kremlin">Yevgeny Prigozhin&rsquo;s Men Poached in Wagner Hiring Spree Linked to Kremlin</a>
      </div>
      '''

soup = BeautifulSoup(html, 'html.parser')
sanitized_output = []

for link in soup.find_all('a'):
    href = link.get('href')
    text = link.string
    sanitized_output.append(f'{text}: {href}')

sanitized_string = "\n".join(sanitized_output)
print(sanitized_string)
