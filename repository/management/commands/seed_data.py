from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from repository.models import Paper


class Command(BaseCommand):
    help = "Seed the database with demo papers"

    def handle(self, *args, **options):
        authors_data = [
            {
                "username": "fondem.c",
                "first_name": "Celestine",
                "last_name": "Fondem",
                "email": "fondem.c@unibamenda.cm",
                "department": "Computer Science",
                "bio": "Senior lecturer in the Department of Computer Science. Research interests include machine learning, distributed systems, and ICT for development.",
            },
            {
                "username": "ngwam.h",
                "first_name": "Herman",
                "last_name": "Ngwam",
                "email": "ngwam.h@unibamenda.cm",
                "department": "Computer Science",
                "bio": "Professor of Computer Science specializing in software engineering, formal methods, and information security.",
            },
            {
                "username": "tchinda.f",
                "first_name": "Flore",
                "last_name": "Tchinda",
                "email": "tchinda.f@unibamenda.cm",
                "department": "Economics",
                "bio": "Lecturer in Economics. Research focuses on development economics, agricultural value chains, and poverty dynamics in Central Africa.",
            },
            {
                "username": "djida.k",
                "first_name": "Armand",
                "last_name": "Djida",
                "email": "djida.k@unibamenda.cm",
                "department": "Economics",
                "bio": "Professor of Economics specializing in econometrics, financial inclusion, and informal sector analysis.",
            },
            {
                "username": "nji.k",
                "first_name": "Kenny",
                "last_name": "Nji",
                "email": "nji.k@unibamenda.cm",
                "department": "Law",
                "bio": "Senior lecturer in Law. Research covers constitutional law, human rights, and decentralisation in Cameroon.",
            },
            {
                "username": "kamgaing.t",
                "first_name": "Thomas",
                "last_name": "Kamgaing",
                "email": "kamgaing.t@unibamenda.cm",
                "department": "Law",
                "bio": "Professor of Law specializing in land tenure, customary law, and access to justice in rural Cameroon.",
            },
            {
                "username": "nkwan.m",
                "first_name": "Mirabel",
                "last_name": "Nkwan",
                "email": "nkwan.m@unibamenda.cm",
                "department": "Public Health",
                "bio": "Lecturer in Public Health. Research interests include maternal health, community health systems, and epidemiological surveillance.",
            },
            {
                "username": "ayuk.p",
                "first_name": "Paul",
                "last_name": "Ayuk",
                "email": "ayuk.p@unibamenda.cm",
                "department": "Public Health",
                "bio": "Professor of Public Health focusing on waterborne diseases, health policy, and One Health approaches in the North West Region.",
            },
        ]

        users = []
        for data in authors_data:
            user, _ = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "email": data["email"],
                },
            )
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "department": data["department"],
                    "bio": data["bio"],
                    "institution": "Scholar Corridor",
                },
            )
            users.append(user)

        papers_data = [
            {
                "title": "Machine Learning Approaches for Crop Disease Detection in the Bamenda Highlands",
                "abstract": "This thesis investigates the application of convolutional neural networks (CNNs) and transfer learning techniques for the early detection and classification of crop diseases prevalent in the Bamenda Highlands region of Cameroon. A novel dataset of 3,200 annotated leaf images was collected from local farms across five growing seasons. The study demonstrates that fine-tuned MobileNetV2 and EfficientNet-B0 architectures achieve classification accuracies of 94.3% and 96.1% respectively, outperforming traditional image processing pipelines. The research further develops a lightweight mobile application prototype enabling farmers to perform real-time disease diagnosis using smartphone cameras, addressing the critical gap in agricultural extension services in the region.",
                "author": users[0],
                "department": "CS",
                "supervisor": "Prof. Herman Ngwam",
                "year": 2025,
                "document_type": "thesis",
                "keywords": "machine learning, crop disease, CNN, transfer learning, agricultural technology",
                "slug": "ml-crop-detection-bamenda-highlands",
                "status": "approved",
            },
            {
                "title": "A Formal Verification Framework for E-Voting Systems in Emerging Democracies",
                "abstract": "This dissertation presents a formal verification framework tailored for electronic voting systems deployed in emerging democratic contexts. Using the Coq proof assistant and model checking with NuSMV, we specify and verify critical security properties including ballot secrecy, vote integrity, and verifiability. The framework is applied to two case studies: the Biometric Voter Registration system used in Cameroon and a proposed blockchain-based voting protocol. Our analysis reveals three previously unknown vulnerabilities in the BVR system and provides formally verified countermeasures. The work contributes a reusable methodology that balances formal rigor with the practical constraints of resource-limited electoral commissions.",
                "author": users[1],
                "department": "CS",
                "supervisor": "Dr. Celestine Fondem",
                "year": 2024,
                "document_type": "dissertation",
                "keywords": "formal verification, e-voting, Coq, model checking, security",
                "slug": "formal-verification-evoting-emerging-democracies",
                "status": "approved",
            },
            {
                "title": "Determinants of Smallholder Cocoa Productivity in the Centre Region of Cameroon: A Quantile Regression Approach",
                "abstract": "This research paper examines the heterogeneous effects of farm inputs, land tenure security, and market access on cocoa productivity across the productivity distribution of smallholders in the Centre Region. Using quantile regression on a stratified sample of 480 farm households, we find that fertilizer use significantly boosts yield at the upper quantiles while land certification has a uniform positive effect across all quantiles. Access to cooperative membership increases productivity primarily for median-performing farms. The results suggest that blanket agricultural policies may be suboptimal and that targeted interventions based on farm performance levels could enhance the competitiveness of Cameroon's cocoa sector.",
                "author": users[2],
                "department": "EC",
                "supervisor": "Prof. Armand Djida",
                "year": 2025,
                "document_type": "research_paper",
                "keywords": "cocoa productivity, quantile regression, smallholder farming, Cameroon",
                "slug": "smallholder-cocoa-productivity-centre-cameroon",
                "status": "approved",
            },
            {
                "title": "Financial Inclusion and Informal Savings Mechanisms in the North West Region of Cameroon",
                "abstract": "This thesis explores the relationship between formal financial inclusion and participation in informal savings groups (njangi) among urban and peri-urban households in the North West Region. Using a mixed-methods approach combining a survey of 620 households and 24 in-depth interviews, the study finds that 73% of formally banked individuals simultaneously participate in njangi groups, citing flexibility, social capital, and trust as primary motivations. A bivariate probit model reveals that formal inclusion and njangi participation are complementary rather than substitutive. The findings challenge the assumption that expanding formal banking displaces informal mechanisms and recommend a hybrid financial architecture that leverages both systems.",
                "author": users[3],
                "department": "EC",
                "supervisor": "Dr. Flore Tchinda",
                "year": 2024,
                "document_type": "thesis",
                "keywords": "financial inclusion, informal savings, njangi, Cameroon, development economics",
                "slug": "financial-inclusion-informal-savings-north-west",
                "status": "approved",
            },
            {
                "title": "Decentralisation and Access to Justice in Rural Cameroon: A Critical Analysis of the 2019 Regional and Local Authorities Law",
                "abstract": "This dissertation critically examines the implications of Law No. 2019/024 on the Decentralisation of Regional and Local Authorities for access to justice in rural Cameroon. Through doctrinal analysis and fieldwork in 12 village communities across the North West and West Regions, the study identifies a persistent gap between the law's aspirational provisions for local dispute resolution and the operational reality on the ground. Customary courts remain underfunded and lack enforcement mechanisms, while the formal court system is geographically and financially inaccessible for most rural residents. The work proposes a tripartite dispute resolution model integrating customary courts, mediation centres, and mobile circuit courts to bridge the access gap.",
                "author": users[4],
                "department": "LW",
                "supervisor": "Prof. Thomas Kamgaing",
                "year": 2025,
                "document_type": "dissertation",
                "keywords": "decentralisation, access to justice, customary courts, Cameroon, rural law",
                "slug": "decentralisation-access-justice-rural-cameroon",
                "status": "approved",
            },
            {
                "title": "Customary Land Tenure Security and Women's Land Rights in the Bamenda Grassfields",
                "abstract": "This research paper investigates the intersection of customary land tenure systems and women's access to land in the Bamenda Grassfields, drawing on 18 months of ethnographic research in three fondoms. The study documents how customary practices of land allocation through lineage heads systematically exclude women from formal land ownership despite their significant role in agricultural production. Analysis of 150 land dispute cases from traditional courts reveals that women succeed in only 23% of land claims. The paper argues that the 2020 Land Tenure Policy reform, while acknowledging gender equity, fails to provide enforceable mechanisms within the customary domain and recommends statutory recognition of women's secondary land rights.",
                "author": users[5],
                "department": "LW",
                "supervisor": "Dr. Kenny Nji",
                "year": 2023,
                "document_type": "research_paper",
                "keywords": "customary land tenure, women land rights, Grassfields, Cameroon, gender equity",
                "slug": "customary-land-tenure-women-bamenda-grassfields",
                "status": "approved",
            },
            {
                "title": "Maternal Health Service Utilisation and Birth Outcomes in the Bamenda Health District: A Retrospective Cohort Study",
                "abstract": "This thesis presents a retrospective cohort study of 2,847 births recorded across 14 health facilities in the Bamenda Health District between 2020 and 2024. The study examines the association between antenatal care attendance, facility-based delivery, and adverse birth outcomes including low birth weight, stillbirth, and maternal near-miss events. Multivariate logistic regression reveals that four or more antenatal visits reduce the odds of low birth weight by 41% (OR 0.59, 95% CI 0.44-0.79) and that facility-based delivery reduces maternal near-miss by 57%. Geographic mapping identifies clusters of poor outcomes in peripheral health areas more than 10 km from the nearest facility, underscoring the need for mobile outreach strategies.",
                "author": users[6],
                "department": "PH",
                "supervisor": "Prof. Paul Ayuk",
                "year": 2025,
                "document_type": "thesis",
                "keywords": "maternal health, antenatal care, birth outcomes, Cameroon, health facility",
                "slug": "maternal-health-birth-outcomes-bamenda-district",
                "status": "approved",
            },
            {
                "title": "Waterborne Disease Surveillance Using One Health Approaches in the Bambili Watershed",
                "abstract": "This dissertation develops and evaluates a One Health surveillance framework for waterborne diseases in the Bambili watershed, integrating human health monitoring, veterinary surveillance, and water quality assessment. Over 18 months, the study collected 360 water samples from 20 sampling points, 1,200 clinical records from three health centres, and 240 animal health reports from local veterinary posts. The integrated analysis identifies significant correlations between E. coli contamination peaks, rainfall events, and diarrhoeal disease incidence 7-14 days later (Spearman r=0.72, p<0.001). The framework reduced outbreak detection time by 63% compared to traditional health-only surveillance. A community-based early warning protocol is proposed for scale-up across the North West Region.",
                "author": users[7],
                "department": "PH",
                "supervisor": "Dr. Mirabel Nkwan",
                "year": 2024,
                "document_type": "dissertation",
                "keywords": "One Health, waterborne disease, surveillance, watershed, Cameroon",
                "slug": "waterborne-disease-one-health-bambili-watershed",
                "status": "approved",
            },
        ]

        for data in papers_data:
            Paper.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )

        # Create a superuser for admin access
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser(
                "admin", "admin@unibamenda.cm", "admin123"
            )
            UserProfile.objects.create(
                user=admin_user,
                department="Administration",
                institution="Scholar Corridor",
            )

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data"))
