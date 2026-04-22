**A SYSTEMATIC REVIEW OF EVENT TECHNOLOGIES IN THE CONTEXT OF SMART
TOURISM: TRENDS AND FUTURE DIRECTIONS**

**ABSTRACT**

This study presents a systematic review of the integration of emerging
digital technologies in smart tourism events, with the purpose of
understanding how technological innovation is transforming event design,
management and visitor experience. The review examines peer-reviewed
journal articles and conference proceedings published between 2014 and
2024 and indexed in the Scopus and Web of Science databases. The
analysis was conducted using the Bibliometrix package in the R
environment, while descriptive and thematic analyses were performed with
the Statistical Package for the Social Sciences. The findings show that
several technological domains, including Artificial Intelligence, the
Internet Of Things, Big Data analytics and immersive technologies, are
driving significant advances in the development of smart tourism events.
These technologies support improvements in personalisation, behavioural
analysis, sustainability, accessibility and real-time decision making.
The review also reveals conceptual fragmentation, methodological
diversity and geographical imbalances across the existing literature.
Overall, this study contributes to consolidating the theoretical
foundations of smart events and identifies promising directions for
future research and innovation within technology-enhanced tourism event
ecosystems.

**KEYWORDS**

Smart Tourism, Emerging Technologies, Artificial Intelligence, Event
Management, Smart Technologies, Systematic Review.

1.  **Introduction**

In recent years, the notion of Smart Tourism has garnered considerable
attention, as the tourism industry has come to adopt technological
advancements with the goal to enhance the visitor experience and promote
sustainable development [(Buhalis & Amaranggana, 2013; Gretzel,
Werthner, et al., 2015; Jovicic, 2019; J. Liu et al., 2024; Pencarelli,
2020; Wael et al., 2023)](https://www.zotero.org/google-docs/?510tgm).
According to [Gretzel et al.
(2015)](https://www.zotero.org/google-docs/?HdpTTa) is a concept that
leverages advanced technologies to transform data from physical
infrastructure, social connections, and organizational sources into
enriched tourism experiences and valuable business propositions, with a
focus on sustainability, efficiency, and personalization.

Extensive research has analysed the multifaceted dimensions of Smart
Tourism, which encompass technological [(Huang et al., 2017; Jeong &
Shin, 2020; Pai et al., 2020, 2025; Um & Chung,
2021)](https://www.zotero.org/google-docs/?gRR1SA), social [(Cacho
et al., 2016; Lam et al., 2020; Liberato et al., 2018; Poli et al.,
2024; Tlili et al., 2021; Zhou et al.,
2024)](https://www.zotero.org/google-docs/?5Bu2n1), economic
[(Kuandykovna Suyendikova et al., 2022; Lee & Hlee, 2021; O'Connor,
2023; Pujakusumah et al., 2024; Shanmugam et al.,
2024)](https://www.zotero.org/google-docs/?HHvQXx), and environmental
aspects [(El Archi et al., 2023; Flores-Crespo et al., 2022; Gelbman,
2020; Hiererra et al., 2023; Saputra,
2023)](https://www.zotero.org/google-docs/?8IIA7K). These interrelated
dimensions collectively contribute to the development of a more
intelligent, sustainable, and efficient tourism ecosystem.

Smart Tourism approaches are applied across a diverse range of contexts
and scenarios, all aimed at enhancing visitor experiences, optimizing
resource management, and promoting sustainability. Key areas of Smart
Tourism implementation include Smart Cities [(Gelbman, 2020; Habeeb &
Weli, 2020; Ismagilova et al., 2019; Khan et al., 2017; Kuandykovna
Suyendikova et al., 2022; Lopes & Oliveira, 2018; Matos et al., 2019;
Parameswaran et al., 2021; Salmi & Hmioui, 2024; Um & Chung, 2021; Wael
et al., 2023)](https://www.zotero.org/google-docs/?sNX7Hf), cultural and
natural heritage sites [(Angelaccio et al., 2013; Balakrishnan et al.,
2023; Berjozkina & Kuruvilla, 2023; Chung et al., 2015, 2018; dos
Santos, 2022; Li et al., 2022; T. T. Nguyen et al., 2017; Oxoli et al.,
2019)](https://www.zotero.org/google-docs/?7risf4), rural destinations
[(Ballina, 2022; Cvar et al., 2024; Inversini et al., 2024; Luo, 2024;
Sustacha et al., 2024; Torabi, Pourtaheri, et al., 2023; Torabi,
Rezvani, et al., 2023)](https://www.zotero.org/google-docs/?HAQ7bh),
shopping districts [(Al-Sulaiti, 2022; Garcia-Milon et al., 2020; Wanyi,
2021)](https://www.zotero.org/google-docs/?yWMmKp), event and festival
venues [(Boodnah et al., 2016; Cimbaljević et al., 2021; Dalli & Bri,
2016; M & P, 2024; T. Nguyen et al., 2020; Sebata & Mollah,
2022)](https://www.zotero.org/google-docs/?rlUxce), transport [(Battarra
et al., 2018; Bogicevic et al., 2017; Burlacu et al., 2022; Marchesani
et al., 2023)](https://www.zotero.org/google-docs/?CJDlxz), or smart
accommodations [(Buhalis et al., 2023; Cumlievski et al., 2022; Gautam
et al., 2017; Pachoulas et al.,
2024)](https://www.zotero.org/google-docs/?FQ6ee4).

In this context, Smart Tourism is characterized as a crucial tool that
harnesses emerging technologies, including the Internet of Things (IoT),
Artificial Intelligence (AI), and Big Data Analytics, to optimize
tourism management and personalize as well as enhance the tourist
experience [(Aliyah et al., 2023; Ferras et al., 2020; Gajdosik &
Marcis, 2019; Kang & Jwa, 2018; Kontogianni et al., 2018; Kontogianni &
Alepis, 2022; Y. Liu & Niu, 2024; Ramos et al., 2016; Stroumpoulis
et al., 2022; Suanpang & Pothipassa,
2024)](https://www.zotero.org/google-docs/?6qEQpi). These technologies
have revolutionized the way various aspects of tourism are managed and
experienced, particularly in dynamic domains such as events, which have
become a pivotal component in attracting visitors, stimulating local
economies, and positioning destinations in an increasingly competitive
and digitalized environment. Events are recognized as crucial components
of tourism from both demand and supply perspectives [(Getz, 2008, 2010;
Getz & Andersson, 2009; Getz & Page, 2024; Gursoy & Kendall, 2006; Tuck
& Xinyi, 2023)](https://www.zotero.org/google-docs/?OptHlQ).

In their research, [Getz & Page
(2014)](https://www.zotero.org/google-docs/?Sytj4P) emphasize the
significance of events within the tourism domain, redefining the concept
of event tourism to encompass a broad range of planned events, including
festivals, sporting competitions, conferences, and mega-events. The
application of smart technologies in events and festivals can
significantly impact various areas, such as visitor management and
safety, event logistics, and environmental sustainability. [Celuch
(2021)](https://www.zotero.org/google-docs/?nsZmwp) examined the role of
Information and Communication Technologies (ICTs) in event management
and their potential for sustainability. His study identifies key areas
for future research, including virtual events, Artificial Intelligence,
Big Data Analytics, and Augmented or Virtual Reality.

Despite the interest in event tourism as a research area, there is a
significant gap in the literature on the application of emerging
technologies in events and festivals. In light of this, this paper
attempts to analyse the concept of Smart Event in the context of Smart
Tourism. The aim is to identify and analyse trends, emerging
technologies and lines of research associated with the term,
particularly in relation to the Smart Event/Smart Music Festival. More
in detail, this study addresses the following research question: "How
have emerging technologies applied to events and festivals evolved
within the context of Smart Tourism?"

To achieve the objective of the study, a systematic literature review
methodology was used. The following sections will describe the
methodology applied in this review. Afterward, a bibliometric analysis
related to the use of emerging technologies in events within the
framework of Smart Tourism will be presented. Next, the most commonly
used technologies in events will be discussed. Then, possible future
research directions in terms of theories, sustainability, and management
strategies will be proposed. Finally, the conclusion will address the
theoretical and practical implications for planning and managing Smart
Events.

Furthermore, this review provides a practical perspective for event
planners, destination managers and marketing professionals, providing
strategies to enhance the impact of events in the context of Smart
Tourism. This includes the possibility of incorporating emerging
technologies, fostering sustainability and maximizing economic and
social return while applying current trends in tourism.

2.  **Methodology**

To conduct a literature review, a systematic methodology is utilized to
locate, select, and evaluate pertinent studies on the given topic, with
the aim of providing a comprehensive understanding of the current state
of knowledge [(Bandara et al., 2015; Fisch & Block, 2018; Xiao & Watson,
2019)](https://www.zotero.org/google-docs/?diLudw). This review followed
a two-stage methodological approach. The first phase entailed the
identification, close reading and comprehensive understanding of
relevant academic sources. The second phase involved a bibliometric
analysis of the selected articles, conducted using SPSS and Biblioshiny
powered by R Studio.

The selected databases were Web of Science (WoS) and Scopus [(Birkle
et al., 2020; Pranckutė,
2021)](https://www.zotero.org/google-docs/?Crqx53). The data collection
process took place between September 2024 and October 2024. To mitigate
potential bias in the study selection, the following inclusion criteria
were established: (1) The studies included in this review were from 2014
to September 2024 and had to directly contribute to the stated research
objective, excluding those with a primary focus outside it. (2) Only
articles and Conference Proceedings indexed in CORE and written in
English were selected. (3) The selected studies focused on the
application of emerging technologies in events or music festivals within
the context of Smart Tourism or on the impact of technological tools on
attendee experience, event management, and sustainability. Studies
addressing other characteristics not related to events or aspects
unrelated to information technology or digitization were excluded.

All selected studies met all three criteria. Additionally, all studies
included in the review were read and evaluated for their alignment with
the research objective.

To conduct a comprehensive literature search for this study, structured
queries were formulated by combining three groupings of search strings:

Grouping 1: events and festivals in the context of Smart Tourism.

Grouping 2: emerging technologies applied to the concept of Smart
Tourism.

Grouping 3: emerging technologies applied to event management.

This grouping strategy aimed to capture a comprehensive range of
relevant studies. The search was conducted across the Web of Science and
Scopus databases, focusing on the title, abstract, and keyword fields
(Table 1).

The construction of the groups involved the use of the \'AND\' operator
to combine the key concepts.

Table 1. Search strings

  -----------------------------------------------------------------------
  EVENTS AND FESTIVALS IN THE CONTEXT OF SMART TOURISM

  \"Smart Tourism\" AND \"Events\"

  \"Smart Tourism\" AND \"Festival\"

  "Smart Cities" AND "Events"

  EMERGINGS TECHNOLOGIES APPLIED TO THE SMART TOURISM CONCEPT

  \"Smart Tourism\" AND \"Artificial Intelligence\"

  \"Smart Tourism\" AND \"Blockchain\"

  \"Smart Tourism\" AND \"Internet of Things\"

  \"Smart Tourism\" AND \"Virtual Reality\"

  \"Smart Tourism\" AND \"Platform\"

  \"Smart Tourism\" AND \"Big Data\"

  EMERGING TECHNOLOGIES APPLIED TO EVENT MANAGEMENT

  \"Crowd Management\"

  \"Event Management\" AND \"Artificial Intelligence\"

  \"Event Management\" AND \"Blockchain\"

  \"Event Management\" AND \"Internet of Things\"

  \"Event Management\" AND \"Virtual Reality\"

  \"Event Management\" AND \"Platform\"

  \"Event Management\" AND \"Big Data\"
  -----------------------------------------------------------------------

Source: Own elaboration

At the end of this phase, the literature search generated 183 records. A
total of 146 remained after eliminating duplicates. 76 of these items
were eliminated because they were not related to the object of the study
or did not meet any of the inclusion criteria. Therefore 58 articles and
12 Proceedings Papers in CORE were retrieved. Of these 70, a cross-check
was carried out to exclude 4 (Figure 1). The reporting format adheres,
with minor adaptations, to the Preferred Reporting Items for Systematic
Reviews and Meta-Analyses (PRISMA) [(Page et al.,
2021)](https://www.zotero.org/google-docs/?m2pZVj).

Figure 1. Literature search overview

![](media/image1.png){width="5.704698162729659in"
height="5.94548009623797in"}

Source: Own elaboration

Table 2. Identified Journals

+-------------------------------------------------------+-----+--------+
| > **Journal title**                                   | >   | > *    |
|                                                       | **C | *Share |
|                                                       | oun | >      |
|                                                       | t** |  (%)** |
+-------------------------------------------------------+-----+--------+
| > ACM Transactions On Intelligent Systems And         | > 1 | > 1,79 |
| > Technology                                          |     |        |
+-------------------------------------------------------+-----+--------+
| > Asia Pacific Journal Of Tourism Research            | > 2 | > 3,57 |
+-------------------------------------------------------+-----+--------+
| > Asian Journal Of Pharmaceutical And Clinical        | > 1 | > 1,79 |
| > Research                                            |     |        |
+-------------------------------------------------------+-----+--------+
| > Case Studies In Fire Safety                         | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Event Management                                    | > 6 | >      |
|                                                       |     |  10,71 |
+-------------------------------------------------------+-----+--------+
| > Expert Systems With Applications                    | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Frontiers In Ecology And Evolution                  | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Frontiers In Psychology                             | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Future Internet                                     | > 2 | > 3,57 |
+-------------------------------------------------------+-----+--------+
| > Ieee Access                                         | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Information Processing & Management                 | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Communication Systems      | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Consumer Studies           | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Contemporary Hospitality   | > 1 | > 1,79 |
| > Management                                          |     |        |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Event And Festival         | > 3 | > 5,36 |
| > Management                                          |     |        |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Hospitality Management     | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Intelligent Systems And    | > 1 | > 1,79 |
| > Applications In Engineering                         |     |        |
+-------------------------------------------------------+-----+--------+
| > International Journal Of Nonlinear Analysis And     | > 1 | > 1,79 |
| > Applications                                        |     |        |
+-------------------------------------------------------+-----+--------+
| > ISPRS International Journal Of Geo-Information      | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Convention & Event Tourism               | > 4 | > 7,14 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Engineering And Applied Sciences         | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Engineering Research                     | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Hospitality And Tourism Technology       | > 3 | > 5,36 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Internet Services And Applications       | > 2 | > 3,57 |
+-------------------------------------------------------+-----+--------+
| > Journal Of Sensors                                  | > 2 | > 3,57 |
+-------------------------------------------------------+-----+--------+
| > Multimedia Tools And Applications                   | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > NEC Technical Journal                               | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Periodica Polytechnica Social And Management        | > 1 | > 1,79 |
| > Sciences                                            |     |        |
+-------------------------------------------------------+-----+--------+
| > Quality And Quantity                                | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Sensors                                             | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Signal Image And Video Processing                   | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Soft Computing                                      | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Sports                                              | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Sustainability                                      | > 2 | > 3,57 |
+-------------------------------------------------------+-----+--------+
| > Tourism Management                                  | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Tourism Management Perspectives                     | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Tourism Planning & Development                      | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Tourism Review                                      | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > Wireless Personal Communications                    | > 1 | > 1,79 |
+-------------------------------------------------------+-----+--------+
| > **Total**                                           | >   | > **10 |
|                                                       | **5 | 0,00** |
|                                                       | 6** |        |
+-------------------------------------------------------+-----+--------+

Source: Own elaboration

The journals in which the articles were surveyed are listed (Table 2).
The articles were exclusively drawn from journals indexed in reputable
bibliometric databases, such as the Journal Citation Report and Scimago
Journal Rank, to ensure the quality of the sampled articles.

Table 3. Identified Conference Proceedings

+------------------------------------------------------+-------+-------+
| **Source**                                           | **    | **    |
|                                                      | ICORE | ICORE |
|                                                      | Sou   | R     |
|                                                      | rce** | ank** |
+------------------------------------------------------+-------+-------+
| ICEIS: Proceedings Of The 19th                       | COR   | C     |
|                                                      | E2018 |       |
| International Conference On Enterprise Information   |       |       |
| Systems - Vol 1                                      |       |       |
+------------------------------------------------------+-------+-------+
| 2018 IEEE International Conference On                | COR   | B     |
|                                                      | E2023 |       |
| Big Data (Big Data)                                  |       |       |
+------------------------------------------------------+-------+-------+
| 34th Australasian Conference On                      | COR   | Au    |
|                                                      | E2018 | stral |
| Information Systems, ACIS 2023                       |       | asian |
+------------------------------------------------------+-------+-------+
| ICC 2020 - 2020 IEEE International                   | COR   | B     |
|                                                      | E2018 |       |
| Conference On Communications (Icc)                   |       |       |
+------------------------------------------------------+-------+-------+
| 16th ACS/IEEE International Conference               | COR   | C     |
|                                                      | E2023 |       |
| On Computer Systems And Applications, AICCSA 2019    |       |       |
+------------------------------------------------------+-------+-------+
| Proceedings Of 2016 IEEE 18th                        | COR   | C     |
|                                                      | E2023 |       |
| International Conference On High Performance         |       |       |
| Computing And Communications;                        |       |       |
|                                                      |       |       |
| Ieee 14th International Conference On Smart City;    |       |       |
| IEEE 2nd International                               |       |       |
|                                                      |       |       |
| Conference On Data Science And Systems               |       |       |
| (HPCC/SMARTCITY/DSS)                                 |       |       |
+------------------------------------------------------+-------+-------+
| 14th International Conference On Mobile              | COR   | Unr   |
|                                                      | E2023 | anked |
| Systems And Pervasive Computing (MOBISPC 2017) /     |       |       |
| 12th International                                   |       |       |
|                                                      |       |       |
| Conference On Future Networks And Communications     |       |       |
| (FNC 2017) / Affiliated                              |       |       |
|                                                      |       |       |
| Workshops                                            |       |       |
+------------------------------------------------------+-------+-------+
| 20th IEEE International Wireless                     | COR   | B     |
|                                                      | E2023 |       |
| Communications And Mobile Computing Conference,      |       |       |
| IWCMC 2024                                           |       |       |
+------------------------------------------------------+-------+-------+
| 37th International Conference On                     | COR   | B     |
|                                                      | E2023 |       |
| Advanced Information Networking And Applications,    |       |       |
| AINA 2023                                            |       |       |
+------------------------------------------------------+-------+-------+
| IEEE International Conference On                     | COR   | B     |
|                                                      | E2023 |       |
| Advanced Learning Technologies                       |       |       |
+------------------------------------------------------+-------+-------+

Source: Own elaboration

The inclusion of Conference Proceedings in this systematic review is
justified by their role in disseminating cutting-edge research on
emerging technologies, particularly in the domains of information
technology and Smart Tourism (Table 3). According to CORE [(Fekete
et al., 2021)](https://www.zotero.org/google-docs/?584bAY), conference
papers capture key trends, present innovative studies prior to journal
publication, and demonstrate rigorous methodologies at relevant academic
conferences. Incorporating these sources ensures a comprehensive and
current analysis of the technological impact on events and festivals in
the context of Smart Tourism.

Table 4. Summary of how each methodological step aligns with the
research objective

  ------------------------------- ---------------------------------------
  **Objective**                   **Methodology**

  1\. Analysis of the temporal    Systematic literature review on Smart
  evolution of scientific         Tourism technologies applied to events
  production                      and festivals.

  2\. Examination of sources,     Systematic literature review on Smart
  countries, methodologies and    Tourism technologies applied to events
  research areas                  and festivals.

  2\. Identification of key       Extraction of recurring technological
  technologies                    trends.

  3\. Proposal of future research Identification of gaps in the
  directions                      literature through thematic analysis.
  ------------------------------- ---------------------------------------

Source: Own elaboration

3.  **Findings**

This section presents the results which are organised as follows: (1)
Analysis of the temporal evolution of scientific production, (2)
Examination of the most influential sources, countries, methodological
contributions and main research areas, (3) Identification of key
emerging event technologies in the context of events in Smart Tourism,
(4) Thematic structure analysis

**3.1 Analysis of the temporal evolution of scientific production**

In order to ensure that this review is grounded in pertinent research,
the authors include an overview of the publication timelines encompassed
in the study. Studies published over the past ten years were included.
This temporal dimension is crucial for understanding the evolution of
research in Smart Tourism in events and festivals, revealing trends in
research focus, the emergence of new themes, and shifts in
methodological approaches that might otherwise remain hidden, thus
providing a valuable perspective on the development of the field.

Figure 2 shows the integration of Smart Tourism technologies in events.
The increasing academic interest in the field can be attributed to the
rising significance of Smart technologies in providing tourism consumers
and service providers with relevant information, improved
decision-making capabilities, enhanced mobility, real-time awareness,
and high-quality and personalized tourism experiences in large-scale
events [(Gretzel, 2011; Luxford & Dickinson,
2015)](https://www.zotero.org/google-docs/?iRLMcO).

Figure 2. Number of publications per year

![](media/image2.png){width="5.880208880139983in"
height="3.44659230096238in"}

Source: Own elaboration

**3.2 Examination of the most influential sources, countries,
methodological contributions and main research areas**

Figure 3. Most relevant sources

![](media/image3.png){width="6.267716535433071in"
height="3.138888888888889in"}

Source: Own elaboration

Figure 3 presents the most significant sources, determined by the number
of documents included in the literature review. This analysis allows for
the identification of journals that have shown the most interest in the
topic, which is essential for understanding the structure of scientific
production in this field.

Event Management stands out as the leading journal, contributing 6
publications and thus demonstrating the highest publication volume. The
Journal of Convention and Event Tourism follows with 4 articles,
succeeded by the International Journal of Event and Festival Management
and the Journal of Hospitality and Tourism Technology, both with 3
articles.

Several sources with comparable publication volumes follow, 2
contributions each, including the Asia Pacific Journal of Tourism
Research, Future Internet, Journal of Internet Services and
Applications, Journal of Sensors, and Sustainability. The remaining
publications have a singular contribution, indicating a more sporadic or
focused interest.

This indicates that, although a significant number of publications
originate from a limited number of specialized sources, there is also
thematic diversification, with technology and sustainability-focused
journals beginning to publish on the subject, likely within
interdisciplinary frameworks such as smart, sustainable, or digital
events.

Figure 4. Source's production over time

![](media/image4.png){width="6.65625in" height="3.3281255468066493in"}

Source: Own elaboration

The temporal analysis (Figure 4) further supports the significance of
Event Management, demonstrating its consistent publication output from
2017 to 2024, thus illustrating its enduring influence in the field.
Other journals, such as the Journal of Convention and Event Tourism and
the Journal of Hospitality and Tourism Technology, have focused their
publications primarily in the years 2023 and 2024, indicating a more
recent focus on the topic.

Figure 5. Country production over time

![](media/image5.png){width="6.267716535433071in"
height="3.138888888888889in"}

Source: Own elaboration

Apart from the temporal analysis of sources, another analysis was
carried out to identify which countries lead scientific production in
this field of knowledge (Figure 5). The data indicates that China is the
foremost contributor to scientific output, exhibiting rapid growth from
2021, and surpassing 20 articles in 2024. The United Kingdom follows,
demonstrating consistent progress since 2015, with a consistent output
of 11 articles. The United States and South Korea have also shown steady
expansion, particularly from 2020, each with over 10 publications. India
has gradually increased its output since 2019, though at a lower volume.
Italy shows more modest growth, though progress has been evident in
recent years. These six countries are the primary contributors to
scientific production during the analyzed period.

Beyond examining the temporal characteristics of scientific production
in terms of countries and sources, it is crucial to examine the
methodological characteristics of the reviewed studies. This approach
enables the identification of not only the evolution of academic
interest, but also the nature of the knowledge generated around the
incorporation of smart technologies in events. Table 5 shows the
research methodologies used. The trend supports the need for meaningful
integration between quantitative and qualitative approaches for a more
comprehensive development of the field [(Provenzano & Baggio,
2019)](https://www.zotero.org/google-docs/?h6n0Kx).

Table 5. Research methodologies

  ------------------------------------------ -------------- -------------
                                             **Count**      **Share**

  Qualitative data analysis                  8              12,1%

  Quantitative data analysis                 46             69,7%

  Mixed methods                              12             18,2%

  **Total**                                  **66**         **100%**
  ------------------------------------------ -------------- -------------

Source: Own elaboration

It has also been analysed whether the studies adopt a theoretical or
empirical approach in order to understand the orientation and
applicability of research in this field. In this regard, 58 articles
(87.9%) were found to be empirical and 8 (12.1%) theoretical. The
predominance of empirical studies indicates a practical orientation in
the research related to the application of Smart technologies in events
and festivals.

This analysis also examined the extent to which the reviewed studies
have developed theoretical models, as this allows for an evaluation of
the level of conceptual development and the contributions to the
theoretical advancement regarding the application of Smart technologies
in events. The analysis reveals that 43 articles (65.2%) develop a
theoretical model and 23 (34.8%) do not. A strong theoretical framework
helps identify the research design and the evaluation of the problem,
offering clarity on how the study has been assembled and allowing the
theory to be tested, measured, and potentially extended [(Grant &
Osanloo, 2015)](https://www.zotero.org/google-docs/?FydP98).

The analysis has identified that the proportion of studies that include
explicit hypotheses as 18 (25,8%). This examination enables the
differentiation between studies focused on validating theoretical
relationships through experimental or statistical methods, and those of
a more exploratory or descriptive nature.

Additionally, Table 6 examines the articles that utilize or provide open
data, enabling an assessment of the transparency, replicability, and
potential for reuse of the research findings in future studies. The use
of open data promotes greater research transparency, allowing other
researchers and practitioners to validate and build upon existing
results [(Numajiri & Hayashi,
2024)](https://www.zotero.org/google-docs/?BXYs3a).

Table 6. Use of open data

  ------------- ---------- ---------------------------------------------------
  **Authors**   **Date**   **Themes**

  Zhang et al.  2021       Optimization of Sports Event Management System
                           Based on Wireless Sensor Network

  Jiang et al   2022       Predicting Citywide Crowd Dynamics at Big Events: A
                           Deep Learning System

  Mu            2022       Digitalization and Information Management Mechanism
                           of Sports Events Based on Cooperative Sensing Model
                           of Multisensor Nodes

  Peckover et   2022       Implementation of Congestion-Related Controls
  al.                      Improves Runner Density, Flow Rate, Perceived
                           Safety, and Satisfaction during an Australian
                           Running Event

  Zhang         2023       Artificial intelligence carbon neutrality strategy
                           in sports event management based on STIRPAT-GRU and
                           transfer learning

  Sui           2024       AI approach on identifying change in public
                           sentiment for major events: Dubai Expo 2020
  ------------- ---------- ---------------------------------------------------

Source: Own elaboration

The distribution of research areas shows a clear dominance of studies
situated within the Social Sciences -- Other Topics, which comprise 21
publications (28.38%), making it the most represented field in the
dataset. This is followed by Computer Science with 12 publications
(16.22%) and Engineering with 10 publications (13.51%), reflecting the
strong technological and computational orientation of current research
in smart tourism and event-related innovation. Telecommunications also
holds a notable presence with 7 publications (9.46%), highlighting the
central role of connectivity infrastructures. Secondary but consistent
contributions come from Business & Economics, Environmental Sciences &
Ecology, and Instruments & Instrumentation, each with 4 publications
(5.41%). The remaining areas, including Education, Imaging Science,
Information Science, Mathematics, Psychology, Physical Geography, Remote
Sensing, Science & Technology (Other Topics), and Sport Sciences, appear
marginally, each contributing 1 publication (1.35%), while Operations
Research & Management Science accounts for 2 publications (2.70%).
Overall, the dataset reflects a socio-technical research structure where
theoretical insights from the social sciences intersect with applied
developments from computing and engineering.

**3.3 Identification of key emerging event technologies in the context
of events in Smart Tourism**

An examination of 66 scholarly articles revealed the identification of
87 nascent technologies (Table 7). Among these, Artificial Intelligence
and Machine Learning are particularly prominent, facilitating
applications such as predictive analytics and the delivery of
personalized visitor experiences. Specifically, deep learning algorithms
contribute to capabilities like crowd forecasting and comprehensive
content analysis. Furthermore, Big Data Analytics plays a crucial role
in supporting real-time decision-making processes and effective crowd
management strategies (Wang & Uysal, 2024; Wan et al., 2021; Wang et
al., 2024; Lu et al., 2024; Hur et al., 2022; Zhang et al., 2021;
Akbarpour et al., 2020; Sui, 2024).

Virtual Reality, Augmented Reality, and Mixed Reality transforms
immersive experiences (Dieck et al., 2021; Hur et al., 2022; Devine et
al., 2024). Internet of Things and sensor networks provide
infrastructure through wireless networks, biometric sensors, and NFC
technology (Sugawara et al., 2022; Mu, 2022; Bustard et al., 2019).
Mobile applications enable user engagement (Kim et al., 2022; Kang &
Jwa, 2018).

Additional technologies include Location-Based Services (Carrino et al.,
2016; Jiang et al., 2022), Cloud Computing (Li et al., 2017; Kubler et
al., 2017), and Crowd Management Systems (Ronchi et al., 2016; Peckover
et al., 2022).

The technological trajectory reveals three distinct developmental
periods: foundational technologies (2015-2017), the advent of Artificial
Intelligence (2018-2020), and the integration of advanced AI with
immersive experiences (2021-2024).

Table 7. Identified technologies

  -------------------------------------------------- ----------- -------------
  **Technology**                                     **Count**   **Share**

  Artificial Intelligence (AI)                       17          19,54%

  Big Data Analytics                                 12          13,79%

  Internet of Things (IoT)                           12          13,79%

  Virtual Reality                                    10          11,49%

  Mobile Applications                                11          12,64%

  Machine Learning (ML)                              7           8,05%

  Artificial Neural Networks                         2           2,30%

  Cloud Computing                                    5           5,75%

  Crowd Management Systems                           4           4,60%

  Deep Learning (DL)                                 3           3,45%

  GPS Data                                           3           3,45%

  Information and Communication Technologies (ICT)   4           4,60%

  Natural Language Processing (NLP)                  3           3,45%

  NFC                                                2           2,30%

  Wearables                                          3           3,45%

  Unmanned Aerial Vehicle (UAV)                      1           1,15%

  Metaverse                                          1           1,15%

  Wireless Sensor Networks                           2           2,30%

  Mixed Reality                                      1           1,15%

  Robotics                                           1           1,15%

  **Total**                                          **87**      **100,00%**
  -------------------------------------------------- ----------- -------------

Source: Own elaboration

**3.4 Thematic structure analysis**

A thematic mapping strategy (Figure 6) was employed to investigate the
strategic placement and evolution of the subjects within the research
domain. The analysis was performed using 100 author's keywords and a
minimum cluster frequency of 5 per thousand documents. The thematic map
is structured based on two dimensions: centrality, which measures a
theme\'s structural importance within the research, and density, which
reflects the theme\'s internal development.

Figure 6. Thematic mapping strategy

![](media/image6.png){width="6.267716535433071in"
height="4.180555555555555in"}

Source: Own elaboration

The thematic mapping strategy delineates a distinct hierarchical
organization of research domains, categorized by their respective stages
of maturation and academic salience. Within the upper-right quadrant,
\'motor themes\' such as tourism, artificial intelligence, and event
technology are prominent, characterized by robust internal consistency
and substantial influence within the scholarly discourse. Conversely,
the upper-left quadrant encompasses \'niche themes,\' including
information and communication technologies, tourism studies, and event
studies. These themes, despite demonstrating considerable development,
exhibit limited integration with the wider thematic landscape. The
lower-right quadrant identifies \'basic themes,\' comprising the
Internet of Things, event management, and tourism management-related
concepts. These represent domains of significant relevance that are
currently nascent in their development, thereby presenting substantial
opportunities for further scholarly inquiry. Lastly, the lower-left
quadrant consolidates \'emerging or declining themes,\' such as crowd
management, Generation Z, sustainability, and event design. These topics
manifest both low thematic density and low centrality, potentially
indicating either nascent conceptualizations or diminished scholarly
focus. Collectively, the analysis underscores a research paradigm
progressively influenced by technological advancements, presenting
extensive avenues for conceptual refinement and empirical investigation.

**4. Conclusion**

This analysis elucidates the transformative impact of emerging
technologies on smart tourism events, revealing how digital innovation
is reshaping event design, management and experiential value. Artificial
Intelligence emerges as a pivotal technological facilitator, supporting
a wide range of applications that span from personalised service
delivery and operational optimisation to enhanced decision-making and
the creation of immersive experiential environments. Alongside
Artificial Intelligence, the Internet of Things, Big Data analytics and
immersive technologies further contribute to the development of dynamic,
responsive and data-driven event ecosystems capable of adapting to
visitor needs in real time.

Furthermore, the continuous expansion of scholarly discourse in recent
years not only signifies intensifying academic interest in smart tourism
but also highlights a progressive shift in research priorities toward
understanding and improving the attendee experience. This growing
emphasis on experience reflects a broader transition in tourism
research, where value creation, personalisation and technological
mediation are increasingly central to theoretical and managerial
debates. Consequently, events are positioned as critical arenas for
examining the complex interplay between technological advancement,
visitor behaviour, perceived value and destination competitiveness.

**4.1 Implications**

This investigation yields significant implications for both theoretical
understanding and practical application. Theoretically, the findings
underscore the imperative to advance and solidify the conceptual
underpinnings of Smart Events, given the extant literature\'s observed
fragmentation and predominant technological orientation. Furthermore,
this review identifies a substantial opportunity to construct
integrative frameworks that bridge technological adoption, visitor
experience, sustainability initiatives, and comprehensive event
management strategies. Practically, the outcomes furnish event planners
and destination managers with actionable insights into leveraging
advanced technologies, including Artificial Intelligence, the Internet
of Things, Big Data analytics, and immersive tools, to augment safety,
operational efficiency, personalization, and sustainability within event
environments. The analysis concurrently emphasizes the critical
necessity of addressing profound ethical and societal considerations,
such as data privacy, digital accessibility, and the equitable
distribution of smart technology benefits (Gretzel et al., 2015).
Collectively, these implications affirm the strategic significance of
smart technologies in shaping the evolutionary trajectory of events
within the broader Smart Tourism ecosystem.

**4.2 Limitations and future research directions**

This systematic review, while providing valuable insights into the
integration of emerging technologies within the Smart Tourism event
context, is subject to several limitations that may have influenced its
findings. The search strategy was confined to Scopus and Web of Science,
encompassing only English-language studies published between 2014 and
2024. This restrictive approach may have inadvertently omitted pertinent
research from other linguistic backgrounds, regional databases, or
earlier foundational scholarship. Furthermore, the review exclusively
considered peer-reviewed journal articles and CORE-indexed conference
proceedings, thereby excluding industry reports and practitioner
literature, which often serve as primary sources for technological
innovation. The underrepresentation of specific event typologies and
geographical regions also curtails the generalizability of the findings.
Lastly, despite the utility of bibliometric tools for thematic
classification, the interpretation of emergent clusters and themes
inherently involves a degree of subjectivity.

Building on these limitations, the extant literature underscores a
burgeoning multidisciplinary interest in the application of nascent
technologies within the context of smart tourism events, revealing
several avenues for further exploration. Researchers advocate for an
expansion of scholarly inquiry through the replication of existing
models across varied event typologies and underrepresented geographical
areas to facilitate the evaluation of technological scalability.
Artificial Intelligence, Big Data, Virtual Reality, and the Internet of
Things are recognized as pivotal facilitators for personalized services,
automated processes, and real-time data analysis. Nevertheless, their
implementation necessitates a meticulous appraisal of associated
concerns, including privacy infringements, security vulnerabilities, and
the imperative of obtaining informed user consent. Furthermore, a number
of scholars advocate for longitudinal investigations to elucidate the
long-term impact of these technologies on visitor satisfaction, loyalty,
and behavioral patterns, thereby encouraging the formulation of more
robust theoretical frameworks that integrate psychological and
situational determinants of experiential evaluation. Concurrently, the
scholarly discourse emphasizes the criticality of assessing the
socio-ethical ramifications of technological integration, with
particular attention to sustainability considerations, digital
accessibility, and potential impacts on marginalized populations.
Lastly, there is a call for the adoption of more comprehensive
methodological paradigms that synthesize qualitative, quantitative, and
computational techniques to more effectively delineate the inherent
complexities of nascent phenomena.

Taken together, these proposals outline an ambitious yet essential
future research agenda that encourages deeper exploration of the
relationship between technological innovation and user experience within
the domain of smart tourism events.

**REFERENCES**

Aliyah, Lukita, C., Pangilinan, G. A., Chakim, M. H. R., & Saputra, D.
B. (2023). Examining the Impact of Artificial Intelligence and Internet
of Things on Smart Tourism Destinations: A Comprehensive Study. *APTISI
Transactions on Technopreneurship* 5(2), 12-22.
https://doi.org/10.34306/att.v5i2sp.332

Al-Sulaiti, I. (2022). Mega shopping malls technology-enabled
facilities, destination image, tourists' behavior and revisit
intentions: Implications of the SOR theory. *Frontiers in Environmental
Science*, 10. https://doi.org/10.3389/fenvs.2022.965642

Angelaccio, M., Basili, A., & Buttarazzi, B. (2013). Using Geo-Business
Intelligence and Social Integration for Smart Tourism Cultural Heritage
Platforms. En S. Reddy & M. Jmaiel (Eds.), *2013 IEEE 22nd international
workshop on enabling technologies: infrastructure for collaborative
enterprises (wetice)* (196-199). https://doi.org/10.1109/wetice.2013.87

Balakrishnan, J., Dwivedi, Y. K., Malik, F. T., & Baabdullah, A. M.
(2023). Role of smart tourism technology in heritage tourism
development. *Journal of Sustainable Tourism*, 31(11), (2506-2525).
https://doi.org/10.1080/09669582.2021.1995398

Ballina, F. J. D. L. B. (2022). Smart Concept In Rural Tourism: A
Comparison Between Two Phases (2016-2019). *Revista de Economia e
Sociologia Rural*, 60(1), 1-15.
https://doi.org/10.1590/1806-9479.2021.234629

Bandara, W., Furtmueller, E., Gorbacheva, E., Miskon, S., & Beekhuyzen,
J. (2015). Achieving Rigor in Literature Reviews: Insights from
Qualitative Data Analysis and Tool-Support. *Communications of the
Association for Information Systems,* 37(1).
https://doi.org/10.17705/1CAIS.03708

Battarra, R., Gargiulo, C., Tremiterra, M. R., & Zucaro, F. (2018).
Smart mobility in Italian metropolitan cities: A comparative analysis
through indicators and actions. *Sustainable Cities and Society*, 41,
556-567. https://doi.org/10.1016/j.scs.2018.06.006

Berjozkina, G., & Kuruvilla, K. J. (2023). Smart tourism and cultural
heritage in the Baltic states: Exploring strategies and tools for
sustainable development. *Worldwide Hospitality And Tourism Themes*,
15(5), (517-527). https://doi.org/10.1108/WHATT-06-2023-0077

Birkle, C., Pendlebury, D. A., Schnell, J., & Adams, J. (2020). Web of
Science as a data source for research on scientific and scholarly
activity. *Quantitative Science Studies*, 1(1), 363-376.
https://doi.org/10.1162/qss_a_00018

Bogicevic, V., Bujisic, M., Bilgihan, A., Yang, W., & Cobanoglu, C.
(2017). The impact of traveler-focused airport technology on traveler
satisfaction. *Technological Forecasting and Social Change*, 123,
(351-361). https://doi.org/10.1016/j.techfore.2017.03.038

Boodnah, K. D., Jaunky, V. C., Armoogum, V., & Armoogum, S. (2016).
Towards Smart Tourism: An Individual Appreciation of Porlwi-By-Light
Festival. *2016 IEEE International Conference On Emerging Technologies
And Innovative Business Practices For The Transformation Of Societies
(EMERGITECH)* (pp. 323-328).

Buhalis, D., & Amaranggana, A. (2013). Smart Tourism Destinations.
Information and communication technologies in tourism 2014, 553-564.
https://doi.org/10.1007/978-3-319-03973-2_40

Buhalis, D., O'Connor, P., & Leung, R. (2023). Smart hospitality: From
smart cities and smart tourism towards agile business ecosystems in
networked destinations. *Information and Communication Technologies in
Tourism* 35(1), (369-393). https://doi.org/10.1108/IJCHM-04-2022-0497

Burlacu, M., Boboc, R. G., & Butilă, E. V. (2022). Smart Cities and
Transportation: Reviewing the Scientific Character of the Theories.
*Sustainability (Switzerland)*, 14(13).
https://doi.org/10.3390/su14138109

Cacho, A., Figueredo, M., Cassio, A., Araujo, M. V., Mendes, L., Lucas,
J., Farias, H., Coelho, J., Cacho, N., & Prolo, C. (2016). Social Smart
Destination: A Platform to Analyze User Generated Content in Smart
Tourism Destinations. *New Advances In Information Systems and
Technologies*, 444, (817-826).
https://doi.org/10.1007/978-3-319-31232-3_77

Celuch, K. (2021a). Event technology for potential sustainable
practices: A bibliometric review and research agenda. *International
Journal of Event and Festival Management,* 12(3), (314-330). Emerald
Group Holdings Ltd. https://doi.org/10.1108/IJEFM-08-2020-0051

Celuch, K. (2021b). Event technology for potential sustainable
practices: A bibliometric review and research agenda. *International
Journal of Event and Festival Management*.
https://doi.org/10.1108/IJEFM-08-2020-0051

Chung, N., Han, H., & Joun, Y. (2015). Tourists' intention to visit a
destination: The role of augmented reality (AR) application for a
heritage site. *Computers in Human Behavior*, 50 (588-599).
https://doi.org/10.1016/j.chb.2015.02.068

Chung, N., Lee, H., Kim, J.-Y., & Koo, C. (2018). The Role of Augmented
Reality for Experience-Influenced Environments: The Case of Cultural
Heritage Tourism in Korea. *Journal of Travel Research*, 57(5), 627-643.
Scopus. https://doi.org/10.1177/0047287517708255

Cimbaljević, M., Stankov, U., Demirović, D., & Pavluković, V. (2021).
Nice and smart: Creating a smarter festival--the study of EXIT (Novi
Sad, Serbia). Asia Pacific Journal of Tourism Research, 26(4), 415-427.
https://doi.org/10.1080/10941665.2019.1596139

Cumlievski, N., Bakaric, M. B., & Matetic, M. (2022). A Smart Tourism
Case Study: Classification of Accommodation Using Machine Learning
Models Based on Accommodation Characteristics and Online Guest Reviews.
*Electronics*, 11(6), 913. https://doi.org/10.3390/electronics11060913

Cvar, N., Stojanova, S., Trilar, J., Kos, A., & Duh, E. S. (2024).
Transformative smart rural tourism in adversity of the COVID-19 pandemic
and beyond. *Journal of Infrastructure, Policy and Development*, 8(6).
https://doi.org/10.24294/jipd.v8i6.4065

Dalli, A., & Bri, S. (2016). Design of Electronic Ticket System for
Smart Tourism. *2016 12th International Conference On Signal-Image
Technology & Internet-Based Systems (SITIS)* (490-492).
https://doi.org/10.1109/SITIS.2016.82

dos Santos, S. R. (2022). Urban spaces of dislocation in Brazilian
cultural heritage city from UNESCO under smart tourism conception.
*PASOS Revista de Turismo y Patrimonio Cultural,* 20(2), 371-387.
https://doi.org/10.25145/j.pasos.2022.20.027

El Archi, Y., Benbba, B., Nizamatdinova, Z., Issakov, Y., Vargane, G.
I., & David, L. D. (2023). Systematic Literature Review Analysing Smart
Tourism Destinations in Context of Sustainable Development: Current
Applications and Future Directions. *Sustainability*, 15(6).
https://doi.org/10.3390/su15065086

Fekete, A., Grundy, J., Garcia De La Banda, M., Winikoff, M., Sadiq, S.,
& Padgham, L. (2021). CORE rankings uses. *ICORE Conference Portal.*

Ferras, X., Louise Hitchen, E., Tarrats-Pons, E., & Arimany Serrat, N.
(2020). Smart Tourism Empowered by Artificial Intelligence: The Case of
Lanzarote. *Journal Of Cases On Information Technology*, 22(1), (1-13).
https://doi.org/10.4018/JCIT.2020010101

Fisch, C., & Block, J. (2018). Six tips for your (systematic) literature
review in business and management research. *Management Review
Quarterly*, 68(2), 103-106. https://doi.org/10.1007/s11301-018-0142-x

Flores-Crespo, P., Bermudez-Edo, M., & Garrido, J. L. (2022). Smart
tourism in Villages: Challenges and the Alpujarra Case Study. *Procedia
Computer Science*, 204, (663-670). Elsevier B.V.
https://doi.org/10.1016/j.procs.2022.08.080

Gajdosik, T., & Marcis, M. (2019). Artificial Intelligence Tools for
Smart Tourism Development. R. Silhavy (Ed.), *Artificial Intelligence
Methods In Intelligent Algorithms* (Vol. 985, pp. 392-402).
https://doi.org/10.1007/978-3-030-19810-7_39

Garcia-Milon, A., Juaneda-Ayensa, E., Olarte-Pascual, C., &
Pelegrin-Borondo, J. (2020). Towards the smart tourism destination: Key
factors in information source use on the tourist shopping journey.
*Tourism Management Perspectives*, 36.
https://doi.org/10.1016/j.tmp.2020.100730

Gautam, B. P., Asami, H., & Batajoo, A. (2017). Cost Effective
Accommodation Planning in a Trip by Using Accomodation Advisor Query
(AA-Query) in STPF. *2017 International Conference On Networking And
Network Applications (NANA)* (330-336).
<https://doi.org/10.1109/NaNA.2017.60>

Gelbman, A. (2020). Smart tourism cities and sustainability. *Geography
Research Forum, 40*(1), (137--148). Ben Gurion University of the Negev.
<https://www.scopus.com/inward/record.uri?eid=2-s2.0-85110514395&partnerID=40&md5=eabf3f243753a0f45d8120029ae56cf4>

Getz, D. (2008). Event tourism: Definition, evolution, and research.
*Tourism Management, 29*(3), (403--428).
<https://doi.org/10.1016/j.tourman.2007.07.017>

Getz, D. (2010). The nature and scope of festival studies.
*International Journal of Event Management Research, 5*(1), (1--47).

Getz, D., & Andersson, T. D. (2009). Sustainable festivals: On becoming
an institution. *Event Management, 12*(1), (1--17).
<https://doi.org/10.3727/152599509787992625>

Getz, D., & Page, S. J. (2014). Progress and prospects for event tourism
research. *Tourism Management, 52*, (593--631).
<https://doi.org/10.1016/j.tourman.2015.03.007>

Getz, D., & Page, S. J. (2024). *Event studies: Theory and management
for planned events* (5.ª ed.). <https://doi.org/10.4324/9781003374251>

Grant, C., & Osanloo, A. (2015). Understanding, selecting, and
integrating a theoretical framework in dissertation research: Developing
a "blueprint" for your house. *Administrative Issues Journal, 4*.
<https://doi.org/10.5929/2014.4.2.9>

Gretzel, U. (2011). Intelligent systems in tourism: A social science
perspective. *Annals of Tourism Research, 38*(3), (757--779).
<https://doi.org/10.1016/j.annals.2011.04.014>

Gretzel, U., Sigala, M., Xiang, Z., & Koo, C. (2015). Smart tourism:
Foundations and developments. *Electronic Markets, 25*(3), (179--188).
<https://doi.org/10.1007/s12525-015-0196-8>

Gretzel, U., Werthner, H., Koo, C., & Lamsfus, C. (2015). Conceptual
foundations for understanding smart tourism ecosystems. *Computers in
Human Behavior, 50*, (558--563).
<https://doi.org/10.1016/j.chb.2015.03.043>

Gursoy, D., & Kendall, K. W. (2006). Hosting mega events: Modeling
locals' support. *Annals of Tourism Research, 33*(3), (603--623).
<https://doi.org/10.1016/j.annals.2006.01.005>

Habeeb, N. J., & Weli, S. T. (2020). Relationship of smart cities and
smart tourism: An overview. *HighTech and Innovation Journal, 1*(4),
(194--202). <https://doi.org/10.28991/HIJ-2020-01-04-07>

Hiererra, S. E., Meyliana, M., Ramadhan, A., & Purnomo, F. (2023). The
requirement aspect for sustainability smart tourism destinations: A
systematic literature review and proposed model analysis. *Journal of
Engineering Science and Technology, 18*(6), (2895--2914).

Huang, C. D., Goo, J., Nam, K., & Yoo, C. W. (2017). Smart tourism
technologies in travel planning: The role of exploration and
exploitation. *Information & Management, 54*(6), (757--770).
<https://doi.org/10.1016/j.im.2016.11.010>

Inversini, A., Aeberli, C., & Talhouk, S. N. (2024). Smart host-guest
relationship in a rural context: The case of Lebanon. *Journal of
Destination Marketing & Management, 31*.
<https://doi.org/10.1016/j.jdmm.2023.100851>

Ismagilova, E., Hughes, L., Dwivedi, Y. K., & Raman, K. R. (2019). Smart
cities: Advances in research---An information systems perspective.
*International Journal of Information Management, 47*, (88--100).
<https://doi.org/10.1016/j.ijinfomgt.2019.01.004>

Jeong, M., & Shin, H. H. (2020). Tourists' experiences with smart
tourism technology at smart destinations and their behavior intentions.
*Journal of Travel Research, 59*(8), (1464--1477).
<https://doi.org/10.1177/0047287519883034>

Jovicic, D. Z. (2019). From the traditional understanding of tourism
destination to the smart tourism destination. *Current Issues in
Tourism, 22*(3), (276--282).
<https://doi.org/10.1080/13683500.2017.1313203>

Kang, H. C., & Jwa, J. W. (2018). Development of android based smart
tourism application based on tourism bigdata analytics. *Journal of
Engineering and Applied Sciences, 13*(5), (1164--1169).
<https://doi.org/10.3923/jeasci.2018.1164.1169>

Khan, M. S., Woo, M., Nam, K., & Chathoth, P. K. (2017). Smart city and
smart tourism: A case of Dubai. *Sustainability, 9*(12).
<https://doi.org/10.3390/su9122279>

Kontogianni, A., & Alepis, E. (2022). AI, Blockchain & Cyber tourism
joining the smart tourism realm. En *13th International Conference on
Information, Intelligence, Systems and Applications (IISA 2022)*.
Institute of Electrical and Electronics Engineers.
<https://doi.org/10.1109/IISA56318.2022.9904393>

Kontogianni, A., Kabassi, K., & Alepis, E. (2018). Designing a smart
tourism mobile application: User modelling through social network user
implicit data. En S. Staab, O. Koltsova, & D. Ignatov (Eds.), *Social
Informatics (SOCINFO 2018), Part II* (pp. 148--158).
<https://doi.org/10.1007/978-3-030-01159-8_14>

Kuandykovna Suyendikova, G., Evgenievich Barykin, S., Mikhailovich
Sergeev, S., Vasilievna Kapustina, I., Krupnov, Y., & Nikolaevna
Shchepkina, N. (2022). Sustainable development of smart cities and smart
territories based on the model of minimizing externalities.
*F1000Research, 11*. <https://doi.org/10.12688/f1000research.114630.2>

Lam, K. L., Chan, C.-S., & Peters, M. (2020). Understanding
technological contributions to accessible tourism from the perspective
of destination design for visually impaired visitors in Hong Kong.
*Journal of Destination Marketing & Management, 17*.
<https://doi.org/10.1016/j.jdmm.2020.100434>

Lee, H., & Hlee, S. (2021). The intra- and inter-regional economic
effects of smart tourism city Seoul: Analysis using an input-output
model. *Sustainability, 13*(7). <https://doi.org/10.3390/su13074031>

Li, D., Du, P., & He, H. (2022). Artificial intelligence-based
sustainable development of smart heritage tourism. *Wireless
Communications & Mobile Computing, 2022*.
<https://doi.org/10.1155/2022/5441170>

Liberato, P., Liberato, D., Abreu, A., Alén, E., & Rocha, Á. (2018).
LGBT tourism: The competitiveness of tourism destinations based on
digital technology. *Advances in Intelligent Systems and Computing,
745*, (264--276). <https://doi.org/10.1007/978-3-319-77703-0_27>

Liu, J., Hall, C. M., Zhu, C., & Cheng, V. T. P. (2024). Redefining the
concept of smart tourism in tourism and hospitality. *Anatolia, 35*(3),
(553--565). <https://doi.org/10.1080/13032917.2023.2282712>

Liu, Y., & Niu, X. (2024). AI virtual travel assistant based on smart
city---An application interface design study. En N. Streitz & S. Konomi
(Eds.), *Distributed, Ambient and Pervasive Interactions, Part I (DAPI
2024)* (pp. 241--254). <https://doi.org/10.1007/978-3-031-59988-0_14>

Lopes, I. M., & Oliveira, P. (2018). The relationship between smart
cities and smart tourism in low density regions. En *2018 13th Iberian
Conference on Information Systems and Technologies (CISTI)*.

Luo, S. (2024). Rural tourism management cloud service platform based on
interactive mobile embedded systems. *International Journal of
Interactive Mobile Technologies, 18*(13), (130--147).
<https://doi.org/10.3991/ijim.v18i13.49065>

Luxford, A., & Dickinson, J. (2015). The role of mobile applications in
the consumer experience at music festivals. *Event Management, 19*.
<https://doi.org/10.3727/152599515X14229071392909>

M, H. S., & P, A. A. (2024). Smart tourism technology, a boon or a bane
for event tourism? In the context of Kochi Muziris Biennale. *Journal of
Convention and Event Tourism, 25*(3), (145--164).
<https://doi.org/10.1080/15470148.2024.2306994>

Marchesani, F., Masciarelli, F., & Bikfalvi, A. (2023). Cities
(r)evolution in the smart era: Smart mobility practices as a driving
force for tourism flow and the moderating role of airports in cities.
*International Journal of Tourism Cities, 9*(4), (1025--1045).
<https://doi.org/10.1108/IJTC-05-2023-0104>

Matos, A., Pinto, B., Barros, F., Martins, S., Martins, J., &
Au-Yong-Oliveira, M. (2019). Smart cities and smart tourism: What future
do they bring? En A. Rocha, H. Adeli, L. Reis, & S. Costanzo (Eds.),
*New Knowledge in Information Systems and Technologies, Vol. 3* (pp.
358--370). <https://doi.org/10.1007/978-3-030-16187-3_35>

Nguyen, T., Lee, K., Chung, N., & Koo, C. (2020). The way generation Y
enjoys a jazz festival: A case of the Korea (Jarasum) music festival.
*Asia Pacific Journal of Tourism Research, 25*(1), (52--63).
<https://doi.org/10.1080/10941665.2019.1580755>

Nguyen, T. T., Camacho, D., & Jung, J. E. (2017). Identifying and
ranking cultural heritage resources on geotagged social media for smart
cultural tourism services. *Personal and Ubiquitous Computing, 21*(2),
(267--279). <https://doi.org/10.1007/s00779-016-0992-y>

Numajiri, H., & Hayashi, T. (2024). Analysis on open data as a
foundation for data-driven research. *Scientometrics, 129*(10),
(6315--6332). <https://doi.org/10.1007/s11192-024-04956-x>

O'Connor, P. (2023). Small- and medium-sized tourism enterprises and
smart tourism: Tourism agenda 2030 perspective article. *Tourism Review,
78*(2), (339--343). <https://doi.org/10.1108/TR-09-2022-0431>

Oxoli, D., Cannata, M., Terza, V., & Brovelli, M. A. (2019). Natural
heritage management and promotion through free and open source software:
A preliminary system design for the Insubriparks project. En M. Brovelli
& A. Marin (Eds.), *FOSS4G 2019---Academic Track* (pp. 179--183).
<https://doi.org/10.5194/isprs-archives-XLII-4-W14-179-2019>

Pachoulas, G., Florou, K., Besarat, J., & Stylios, C. (2024). Enhancing
visitor experience and hospitality in accommodation facilities through
smart tourism and mobile technology. *SEEDA-CECNSM 2024*, (36--41).
<https://doi.org/10.1109/SEEDA-CECNSM63478.2024.00016>

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T.
C., Mulrow, C. D., ... Moher, D. (2021). The PRISMA 2020 statement: An
updated guideline for reporting systematic reviews. *BMJ, 372*, (n71).
<https://doi.org/10.1136/bmj.n71>

Pai, C.-K., Chen, H., Lai, I. K. W., & Li, T. (2025). Assessing the
quality of smart tourism technology: Development and validation of a
measurement scale. *Journal of Hospitality and Tourism Technology*.
<https://doi.org/10.1108/JHTT-01-2024-0013>

Pai, C.-K., Liu, Y., Kang, S., & Dai, A. (2020). The role of perceived
smart tourism technology experience for tourist satisfaction, happiness
and revisit intention. *Sustainability, 12*(16).
<https://doi.org/10.3390/su12166592>

Parameswaran, A. N., Shivaprakasha, K. S., & Bhandarkar, R. (2021).
Smart tourism development in a smart city: Mangaluru. *Smart Innovation,
Systems and Technologies, 213 SIST* (pp. 325--332). Springer.
<https://doi.org/10.1007/978-981-33-4443-3_31>

Pencarelli, T. (2020). The digital revolution in the travel and tourism
industry. *Information Technology and Tourism, 22*(3), (455--476).
<https://doi.org/10.1007/s40558-019-00160-3>

Poli, M., Malagas, K., & Papakostas, C. (2024). The contribution of
advanced technologies to the tourism experience of disabled people: The
Greek case. *Lecture Notes in Networks and Systems, 1170*, (429--442).
<https://doi.org/10.1007/978-3-031-73344-4_36>

Pranckutė, R. (2021). Web of Science (WoS) and Scopus: The titans of
bibliographic information in today's academic world. *Publications,
9*(1). <https://doi.org/10.3390/publications9010012>

Provenzano, D., & Baggio, R. (2019). Quantitative methods in tourism and
hospitality: A perspective article. *Tourism Review, 75*(1), (24--28).
<https://doi.org/10.1108/TR-07-2019-0281>

Pujakusumah, R., Tonang, A. S. P. A., & Mutaqin, J. N. (2024). Smart
tourism destinations of Sumedang Regency: Future trends and challenges.
*ICISS 2024 Proceedings*.
<https://doi.org/10.1109/ICISS62896.2024.10751014>

Ramos, C. M. Q., Henriques, C. H. N., & Lanquar, R. (2016). Augmented
reality for smart tourism in religious heritage itineraries: Tourism
experiences in the technological age. En *Handbook of Research on
Human-Computer Interfaces, Developments, and Applications*. IGI Global.
<https://doi.org/10.4018/978-1-5225-0435-1.ch010>

Salmi, K., & Hmioui, A. (2024). The smart tourist destination as a smart
city project. En F. Y., H. A., S. T., T. H., & V. A. (Eds.), *Lecture
Notes in Networks and Systems, 838 LNNS* (pp. 222--228). Springer.
<https://doi.org/10.1007/978-3-031-48573-2_32>

Saputra, R. A. (2023). Economic improvement, environmental
sustainability, and community empowerment in Indonesia: Bibliometric
analysis (smart city and smart tourism) 2013--2022. *E3S Web of
Conferences, 440*. EDP Sciences.
<https://doi.org/10.1051/e3sconf/202344001006>

Sebata, E., & Mollah, M. R. A. (2022). Technology application in tourism
festivals in Asia: Theoretical discussions. *Technology Application in
Tourism Fairs, Festivals and Events in Asia*.
<https://doi.org/10.1007/978-981-16-8070-0_2>

Shanmugam, K., Rana, M. E., & Kong, Z. Y. (2024). A comprehensive
analysis of technological advancements and smart tourism strategies in
Malaysia's post-pandemic tourism industry. *ICETSIS 2024*, (909--916).
<https://doi.org/10.1109/ICETSIS61505.2024.10459443>

Stroumpoulis, A., Kopanaki, E., & Varelas, S. (2022). Role of artificial
intelligence and big data analytics in smart tourism: A resource-based
view approach. *WIT Transactions on Ecology and the Environment, 256*
(pp. 99--108). WITPress. <https://doi.org/10.2495/ST220091>

Suanpang, P., & Pothipassa, P. (2024). Integrating generative AI and IoT
for sustainable smart tourism destinations. *Sustainability, 16*(17).
<https://doi.org/10.3390/su16177435>

Sustacha, I., Baños-Pino, J. F., & Del Valle, E. (2024). How smartness
affects customer-based brand equity in rural tourism destinations.
*Journal of Destination Marketing & Management, 34*.
<https://doi.org/10.1016/j.jdmm.2024.100949>

Tlili, A., Altinay, F., Altinay, Z., & Zhang, Y. (2021). Envisioning the
future of technology integration for accessible hospitality and tourism.
*International Journal of Contemporary Hospitality Management, 33*(12),
(4460--4482). <https://doi.org/10.1108/IJCHM-03-2021-0321>

Torabi, Z.-A., Pourtaheri, M., Hall, C. M., Sharifi, A., & Javidi, F.
(2023). Smart tourism technologies, revisit intention, and word-of-mouth
in emerging and smart rural destinations. *Sustainability, 15*(14).
<https://doi.org/10.3390/su151410911>

Torabi, Z.-A., Rezvani, M. R., Hall, C. M., & Allam, Z. (2023). On the
post-pandemic travel boom: How capacity building and smart tourism
technologies in rural areas can help---Evidence from Iran.
*Technological Forecasting and Social Change, 193*.
<https://doi.org/10.1016/j.techfore.2023.122633>

Um, T., & Chung, N. (2021). Does smart tourism technology matter?
Lessons from three smart tourism cities in South Korea. *Asia Pacific
Journal of Tourism Research, 26*(4), (396--414).
<https://doi.org/10.1080/10941665.2019.1595691>

Wael, R., Talaat, H., & Soubra, H. (2023). Smart tourism in smart
cities: Current trends and future challenges in sustainability and
digitization. *Smart Cities 4.0 2023*, (95--98).
<https://doi.org/10.1109/SmartCities4.056956.2023.10526099>

Wanyi, X. (2021). Research on data mining of smart tourism e-commerce
based on data mining model. *ACM International Conference Proceeding
Series* (pp. 361--364). <https://doi.org/10.1145/3516529.3516602>

Xiao, Y., & Watson, M. (2019). Guidance on conducting a systematic
literature review. *Journal of Planning Education and Research, 39*(1),
(93--112). <https://doi.org/10.1177/0739456X17723971>

Zhou, L., Buhalis, D., Fan, D. X. F., Ladkin, A., & Lian, X. (2024).
Attracting digital nomads: Smart destination strategies, innovation and
competitiveness. *Journal of Destination Marketing & Management, 31*.
<https://doi.org/10.1016/j.jdmm.2023.100850>
