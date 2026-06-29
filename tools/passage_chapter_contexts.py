from __future__ import annotations

CHAPTER_CONTEXTS: dict[tuple[str, str], list[str]] = {
    ("1 Corinthians", "14"): [
        "In **1 Corinthians 14**, Paul is correcting disorder in the gathered church. The whole chapter is governed by intelligibility, order, and edification, so individual instructions in the chapter must be read within that larger concern for building up the body.",
    ],
    ("1 Corinthians", "3"): [
        "In **1 Corinthians 3**, Paul addresses a divided church that is thinking in worldly terms about leaders and status. The chapter moves from Christ as the only true foundation to the corporate people of God as His temple, so its warnings and promises concern the church's life in Christ rather than private spirituality detached from the body.",
    ],
    ("1 John", "1"): [
        "In **1 John 1**, John opens the letter by grounding fellowship with God in the apostolic witness about the Word of life. The chapter contrasts walking in the light with false claims about sinlessness, so its statements about confession, cleansing, and fellowship must be read within that truth-versus-falsehood framework.",
    ],
    ("1 John", "5"): [
        "In **1 John 5**, John is drawing the letter toward its conclusion by stressing life in the Son, assurance, and confidence before God. The chapter ties prayer, obedience, and discernment together, so verses here should be read in light of the whole letter's concern for abiding in Christ and walking in the truth.",
    ],
    ("1 Peter", "2"): [
        "In **1 Peter 2**, Peter explains what it means for believers to come to Christ as living stones and to be formed into a holy people. The chapter emphasizes identity, priesthood, witness, and conduct before the world, so its key images describe the church's corporate calling under Christ.",
    ],
    ("1 Peter", "3"): [
        "In **1 Peter 3**, Peter is teaching believers how to endure suffering with a good conscience while following Christ's example. The chapter's discussion of baptism is tied to Christ's death, resurrection, and triumph, not to empty outward ritual divorced from the appeal of a cleansed conscience toward God.",
    ],
    ("1 Samuel", "1"): [
        "In **1 Samuel 1**, the narrative centers on Hannah's distress, her prayer before the Lord, and the birth of Samuel. The chapter is not merely about private desire being granted; it sets up God's larger work in Israel through the child who will become prophet, judge, and pivotal figure in the transition toward monarchy.",
    ],
    ("1 Samuel", "2"): [
        "In **1 Samuel 2**, Hannah's prayer responds to the Lord's action with praise centered on His holiness, sovereignty, and power to reverse human expectations. The chapter widens the story from one family to God's rule over the proud and the humble across Israel's history.",
    ],
    ("1 Thessalonians", "5"): [
        "In **1 Thessalonians 5**, Paul closes the letter with a rapid series of exhortations for sober, watchful, Spirit-sensitive Christian living. The chapter binds prayer, gratitude, discernment, testing, and holiness together, so its short commands belong to a larger picture of a church living in readiness for the Lord.",
    ],
    ("2 Corinthians", "11"): [
        "In **2 Corinthians 11**, Paul is defending the Corinthians against false apostles by exposing the danger of spiritual deception and counterfeit appearances. The chapter warns that outward impressiveness is no guarantee of truth, because deception often comes clothed in religious form.",
    ],
    ("2 Corinthians", "12"): [
        "In **2 Corinthians 12**, Paul moves from revelations to weakness, showing that divine power is displayed not through self-exaltation but through dependence on God's grace. The chapter reframes suffering and unanswered requests through the lens of God's purpose rather than human preference.",
    ],
    ("2 Corinthians", "5"): [
        "In **2 Corinthians 5**, Paul speaks about life between the present age and the coming fullness of resurrection glory. The chapter is saturated with faith, hope, reconciliation, and the unseen realities of belonging to Christ, so its famous lines must be read in that eschatological and gospel-centered frame.",
    ],
    ("Acts", "10"): [
        "In **Acts 10**, Luke records the opening of the gospel to Gentiles through Peter's encounter with Cornelius. The chapter's events show God's initiative, the Spirit's freedom, and the church's need to recognize that God is receiving those who believe, not merely those who fit prior expectations.",
    ],
    ("Acts", "2"): [
        "In **Acts 2**, Pentecost marks the outpouring of the Spirit, Peter's proclamation of the risen Christ, and the first great response to the gospel. The chapter holds repentance, baptism, forgiveness, Spirit, and entry into the new covenant community together within the birth of the church.",
    ],
    ("Acts", "22"): [
        "In **Acts 22**, Paul is giving his defense in Jerusalem by recounting his conversion and commission. The chapter is autobiographical and covenantal at once, showing how the risen Christ interrupted Paul's former life and redirected him into obedience and witness.",
    ],
    ("Acts", "4"): [
        "In **Acts 4**, the apostles face threats after proclaiming Christ publicly, and the church responds together in prayer. The chapter is framed by opposition, bold witness, and the sovereign rule of God, so its prayer language is bound to mission rather than self-protection.",
    ],
    ("Acts", "8"): [
        "In **Acts 8**, the gospel is moving beyond Jerusalem, and Philip's ministry among the Samaritans and the Ethiopian shows the widening reach of Christ's kingdom. The chapter's baptism scenes belong to that outward expansion of the gospel and the immediate obedience of those who receive it.",
    ],
    ("Colossians", "1"): [
        "In **Colossians 1**, Paul magnifies the supremacy of Christ and prays that believers would walk in a manner worthy of Him. The chapter ties knowledge, spiritual fruit, endurance, redemption, and Christ's cosmic lordship together into one unified vision of Christian life.",
    ],
    ("Deuteronomy", "18"): [
        "In **Deuteronomy 18**, Moses distinguishes Israel sharply from pagan nations by forbidding occult and divinatory practices. The chapter sets covenant faithfulness against every attempt to seek spiritual guidance apart from the Lord's own appointed word.",
    ],
    ("Deuteronomy", "19"): [
        "In **Deuteronomy 19**, Moses gives laws meant to preserve justice and truth within Israel's covenant life. The chapter's witness standard belongs to that broader concern that judgment must rest on established testimony rather than private accusation or impulse.",
    ],
    ("Didache", "7"): [
        "The **Didache** is an early Christian church document, not part of the biblical canon, but historically useful for seeing how some early believers described practice. Chapter 7 concerns baptismal instruction and therefore belongs in a historical, not scriptural, supporting context.",
    ],
    ("Ephesians", "2"): [
        "In **Ephesians 2**, Paul contrasts humanity's former death in sin with God's saving action in Christ. The chapter binds grace, faith, new creation, and the making of one new people together, so its statements about salvation belong inside the whole gospel movement from death to life.",
    ],
    ("Ephesians", "3"): [
        "In **Ephesians 3**, Paul reflects on the revealed mystery of Christ and then prays for believers to be strengthened inwardly and filled with the fullness of God. The chapter places prayer inside the vast scope of God's redemptive purpose in Christ and in His church.",
    ],
    ("Ephesians", "4"): [
        "In **Ephesians 4**, Paul moves from doctrine to conduct, calling the church to unity, maturity, holiness, and truthfulness. References to the Spirit in this chapter belong to that corporate and ethical transformation rather than to isolated emotional experience.",
    ],
    ("Ephesians", "6"): [
        "In **Ephesians 6**, Paul closes with the armor of God and a call to persevering prayer in the midst of spiritual conflict. The chapter treats prayer as part of steadfast gospel warfare, endurance, and bold witness.",
    ],
    ("Galatians", "3"): [
        "In **Galatians 3**, Paul argues fiercely that justification and sonship come through faith in Christ rather than works of the law. The chapter connects promise, faith, union with Christ, and covenant identity, so its baptism language belongs inside Paul's gospel argument about belonging to Christ.",
    ],
    ("Galatians", "6"): [
        "In **Galatians 6**, Paul turns to the practical life that should flow from the gospel he has defended throughout the letter. The chapter stresses mutual burden-bearing, humility, sowing and reaping, and life in the new creation.",
    ],
    ("Genesis", "12"): [
        "In **Genesis 12**, the Lord's call and promise to Abram begin the covenant story in earnest, yet the chapter also records Abram's failure under pressure in Egypt. Its movement from promise to fear to divine preservation shows both God's faithfulness and human weakness.",
    ],
    ("Genesis", "16"): [
        "In **Genesis 16**, Abram and Sarai respond to delay in God's promise by taking matters into their own hands through Hagar. The chapter exposes the pain and disorder that follow when people try to secure God's promise by human strategy.",
    ],
    ("Genesis", "26"): [
        "In **Genesis 26**, Isaac faces famine under the shadow of the promises first given to Abraham. The chapter shows the Lord directing, preserving, and blessing Isaac, highlighting the contrast between divine guidance and fearful self-management.",
    ],
    ("Hebrews", "11"): [
        "In **Hebrews 11**, the writer surveys the saints of old to show what faith looks like in action across redemptive history. The chapter's point is not vague optimism but steadfast trust in God and in realities not yet seen.",
    ],
    ("Hebrews", "4"): [
        "In **Hebrews 4**, the writer presses the church to enter God's rest by faith rather than hardening the heart. The chapter binds the living Word of God, exposure before Him, and confidence in Christ our great high priest into one searching call to perseverance.",
    ],
    ("James", "4"): [
        "In **James 4**, James confronts quarrels, worldly desire, pride, and double-mindedness among believers. His comments about asking and not receiving sit inside that larger rebuke of self-seeking and divided loyalties before God.",
    ],
    ("James", "5"): [
        "In **James 5**, James closes the letter by addressing suffering, patience, oaths, confession, and prayer in the life of the community. The chapter presents prayer in the setting of endurance, restoration, righteousness, and life together before God.",
    ],
    ("Jeremiah", "29"): [
        "In **Jeremiah 29**, the Lord speaks to exiles already in Babylon, commanding them to live faithfully there while awaiting His appointed restoration. The chapter is covenantal and historical, not a free-floating promise detached from exile, judgment, and God's long-range purpose for His people.",
    ],
    ("John", "1"): [
        "In **John 1**, the Gospel opens by identifying Jesus as the eternal Word through whom all things were made and who became flesh. The chapter establishes from the start that everything to follow must be read in light of Christ's divine identity, revelation, and saving mission.",
    ],
    ("John", "11"): [
        "In **John 11**, Jesus raises Lazarus in the climactic sign that leads directly toward the final conflict before His death. The chapter holds grief, delay, glory, resurrection, and faith together, showing that Jesus acts according to the Father's purpose even when that purpose is not immediately understood.",
    ],
    ("John", "13"): [
        "In **John 13**, Jesus prepares His disciples for His departure by washing their feet, exposing betrayal, and commanding them to love one another. The chapter frames Christian identity around the pattern and love of Christ Himself.",
    ],
    ("John", "14"): [
        "In **John 14**, Jesus is comforting His disciples on the night before the cross and teaching them about the Father's house, His own identity, and the coming help of the Spirit. Promises about asking in His name belong inside that farewell context of union with Christ, obedience, and divine mission.",
    ],
    ("John", "15"): [
        "In **John 15**, Jesus uses the vine and branches to teach abiding, fruitfulness, obedience, love, and dependence on Him. Requests in this chapter are framed by ongoing union with Christ, not by detached human wishing.",
    ],
    ("John", "16"): [
        "In **John 16**, Jesus continues preparing the disciples for His death, resurrection, departure, and the coming of the Spirit. Its promises about prayer and joy are part of that transition into the new covenant reality of life in His name.",
    ],
    ("John", "20"): [
        "In **John 20**, the risen Christ appears to His disciples and confronts both fear and unbelief with resurrection reality. The chapter's treatment of seeing and believing belongs to John's larger purpose that readers may believe Jesus is the Christ and have life in His name.",
    ],
    ("John", "3"): [
        "In **John 3**, John's Gospel brings together new birth, the Spirit, faith, and witness to Christ. Even narrative details in the chapter should be read within that wider testimony to what it means to receive life from above.",
    ],
    ("John", "4"): [
        "In **John 4**, Jesus reveals Himself beyond old covenant boundaries through His encounter with the Samaritan woman and His teaching about true worship. The chapter shifts attention away from sacred geography and toward worship shaped by truth and the Spirit.",
    ],
    ("John", "6"): [
        "In **John 6**, Jesus moves from the feeding of the multitude into the Bread of Life discourse, where material bread becomes the doorway into deeper revelation about Himself. The chapter is intentionally interpretive: it takes a physical sign and presses the reader toward Christ as the true and lasting source of life.",
    ],
    ("Luke", "11"): [
        "In **Luke 11**, Jesus teaches on prayer and then explains the Father's goodness in giving what is truly needed. The chapter's promise language is framed by the Lord's Prayer, persistence in seeking, and the climactic gift of the Holy Spirit.",
    ],
    ("Luke", "17"): [
        "In **Luke 17**, Jesus teaches about stumbling, forgiveness, faith, gratitude, and the coming of the kingdom. His words about the kingdom must be read against false expectations of spectacle and external signs alone.",
    ],
    ("Luke", "18"): [
        "In **Luke 18**, Jesus teaches persistence in prayer, humility before God, and faith that endures while awaiting His vindication. The chapter is shaped by justice, dependence, and the question of whether faith will remain when the Son of Man comes.",
    ],
    ("Luke", "23"): [
        "In **Luke 23**, Jesus is on the cross and approaching death, yet He continues to speak and act in perfect trust toward the Father. The chapter's sayings from the cross reveal both the depth of suffering and the steadfastness of Christ's obedience.",
    ],
    ("Mark", "10"): [
        "In **Mark 10**, Jesus is teaching about discipleship, dependence, and the reversal of worldly expectations on the road to Jerusalem. Individual healings in the chapter are tied to faith, sight, and following Jesus in the way of the cross.",
    ],
    ("Mark", "11"): [
        "In **Mark 11**, Jesus enters Jerusalem as king, judges the temple order, and uses the fig tree as a living sign of fruitless religion under judgment. The chapter's teaching on prayer is inseparable from that prophetic setting of faith, judgment, forgiveness, and divine purpose.",
    ],
    ("Mark", "16"): [
        "In **Mark 16**, the resurrection stands at the center, and the longer ending has long been discussed because of its textual history. Any use of this chapter should distinguish clearly between the resurrection message itself and questions surrounding the longer textual ending.",
    ],
    ("Matthew", "12"): [
        "In **Matthew 12**, Jesus exposes hardened unbelief in the face of clear revelation and warns against a generation that demands signs while resisting repentance. The chapter contrasts genuine recognition of God's work with hostile spiritual blindness.",
    ],
    ("Matthew", "16"): [
        "In **Matthew 16**, Jesus rebukes those who demand signs, reveals the significance of Peter's confession, and begins preparing the disciples for His suffering and death. The chapter joins discernment, messianic identity, and the necessity of the cross.",
    ],
    ("Matthew", "18"): [
        "In **Matthew 18**, Jesus teaches His disciples about humility, stumbling, restoration, forgiveness, and life together in His kingdom. Its language about agreement, witnesses, and gathered presence belongs to this communal and disciplinary context, not to isolated proof-texting.",
    ],
    ("Matthew", "26"): [
        "In **Matthew 26**, the passion narrative tightens around betrayal, sorrow, submission, and the approach of the cross. Gethsemane is the setting in which Jesus' prayer reveals both the reality of His suffering and the perfection of His submission to the Father's will.",
    ],
    ("Matthew", "27"): [
        "In **Matthew 27**, Jesus suffers, is crucified, and dies under the weight of redemptive judgment. The chapter's cry from the cross must be read in the larger scriptural and covenantal frame of the passion, not as a denial of the Father's plan.",
    ],
    ("Matthew", "28"): [
        "In **Matthew 28**, the risen Christ commissions His disciples with all authority in heaven and on earth. The chapter places disciple-making, baptism, teaching, and Christ's abiding presence together at the climax of the Gospel.",
    ],
    ("Matthew", "6"): [
        "In **Matthew 6**, part of the Sermon on the Mount, Jesus contrasts hypocritical religion with true life before the Father. The chapter moves through giving, prayer, fasting, treasure, anxiety, and kingdom-seeking, so every individual saying must be read inside that unified call to trust the Father and seek His will first.",
    ],
    ("Matthew", "7"): [
        "In **Matthew 7**, Jesus continues the Sermon on the Mount by calling His hearers to discernment, persistence, obedience, and a life built on His words. Promises about asking are framed by the Father's goodness and by the wider demands of kingdom life.",
    ],
    ("Matthew", "9"): [
        "In **Matthew 9**, Jesus' healing ministry reveals His authority to forgive, restore, and call sinners. Acts of healing in the chapter are repeatedly tied to faith and to the arrival of the kingdom in His person.",
    ],
    ("Philippians", "1"): [
        "In **Philippians 1**, Paul writes from imprisonment with joy rooted in the advance of the gospel and the work of Christ in His people. His prayers in the chapter are shaped by spiritual growth, discernment, and fruit that glorifies God.",
    ],
    ("Philippians", "4"): [
        "In **Philippians 4**, Paul closes with exhortations to joy, peace, prayer, contentment, and gospel partnership. The chapter treats provision in the context of Christ-centered contentment and sacrificial support for ministry, not detached prosperity promises.",
    ],
    ("Proverbs", "3"): [
        "In **Proverbs 3**, wisdom is presented as a way of life marked by trust, humility, correction, and submission to the Lord's ordering of the path. Its language about trusting and acknowledging God belongs to a whole chapter about wise dependence rather than self-direction.",
    ],
    ("Psalm", "22"): [
        "Psalm 22 moves from abandonment and suffering into vindication and praise before the nations. When its opening cry appears on Jesus' lips, the whole psalm stands behind the citation, not merely its first line in isolation.",
    ],
    ("Psalm", "31"): [
        "Psalm 31 is a prayer of trust from the midst of distress, slander, and danger. Its language of entrusting oneself to God belongs to a larger movement of refuge, deliverance, and steadfast confidence in the Lord.",
    ],
    ("Psalm", "46"): [
        "Psalm 46 proclaims God's presence and stability when nations rage and the earth shakes. Its stillness language belongs to a psalm about God's sovereign rule and refuge, not to a merely inward or sentimental quietism.",
    ],
    ("Romans", "10"): [
        "In **Romans 10**, Paul is explaining righteousness by faith, the nearness of the word, and the necessity of confession and belief in Christ. The chapter belongs to his larger argument about the gospel, Israel, and salvation through faith rather than law.",
    ],
    ("Romans", "15"): [
        "In **Romans 15**, Paul is bringing together exhortation, mission, and his travel plans as he nears the close of the letter. His prayer request there must be read within apostolic service, gospel labor, and submission to God's will rather than private convenience.",
    ],
    ("Romans", "6"): [
        "In **Romans 6**, Paul explains what union with Christ means for sin, death, and newness of life. The chapter's statements about baptism, slavery, freedom, and life under grace all serve the larger claim that those joined to Christ must no longer live as they once did.",
    ],
    ("Romans", "8"): [
        "In **Romans 8**, Paul unfolds life in the Spirit, the believer's adoption, suffering, hope, and the unbreakable purpose of God in Christ. Its teaching on prayer belongs to that larger assurance that God is at work even in weakness and groaning.",
    ],
}
