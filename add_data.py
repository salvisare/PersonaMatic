# add_data.py
from app import create_app, db
from app.models.users import User
from app.models.user_uploaded_data import UserUploadedData
from datetime import datetime

# Create an app instance
app = create_app()

def add_uploaded_data(user_id, persona_id, file_name, file_type, content):
    # Create a new UserUploadedData instance
    new_uploaded_data = UserUploadedData(
        user_id=user_id,
        persona_id=persona_id,
        file_name=file_name,
        file_type=file_type,
        content=content,  # Content is the text data you're adding
        uploaded_at=datetime.utcnow(),
        processed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Add to the session and commit to the database
    db.session.add(new_uploaded_data)
    db.session.commit()

    print("New uploaded data added successfully!")


# Add data to the "content" field in UserUploadedData table
with app.app_context():  # Push the application context
    # Create a new user uploaded data record
    new_uploaded_data = UserUploadedData(
        user_id=1,  # Assuming a user with ID 1 exists
        persona_id=1,  # Assuming a persona with ID 1 exists
        file_name="example_file.txt",
        file_type="text/plain",
        content="From fruit hawker to award-winning lemon farmer Wayne Mansfield (33), winner of the 2018 Western Cape New Entrant to Commercial Agriculture Award, is one of those overnight successes that was preceded by decades of hard work. Although he won this prestigious award from Agricultural Writers SA after being a farmer for just three years, he started working towards it in primary school, folding boxes for his family’s fruit hawking business. The tiny town of Pniel, nestled at the foot of the Simonsberg mountain outside Stellenbosch in the Western Cape, is where Mansfield was born and raised. The Mansfield family’s laatlammetjie (a child born many years after its siblings) admits that when growing up he wasn’t very book smart, but his knack for business grew quickly. Enrolled in Pniel Primary, he says; I opted for days at home working over sitting behind a school desk. I really didn’t like going to school, to be honest, struggling to focus. And when my parents got me tested they discovered that I was dyslexic. This never deterred Mansfield, because his father, John, soon picked up that his son worked well with his hands. During school holidays I would help my parents fold boxes to package fruit they sold to the Cape Town markets. I was probably in grade 2 when I started working with them.Mansfield credits his success today to how he was raised, his exposure to the industry and the sound values his parents taught him. It costs absolutely nothing to greet anyone nicely and to ask how they’re doing. Just to be kind, he says. Growing up wasn’t easy, Mansfield shared. I know what it feels like to struggle, but we came through that. We never went to bed hungry, but we didn’t have fancy things and some days were more difficult than others. Throughout his schooling Mansfield continued to work for his uncle who was a salesman on the Cape Town market to make extra pocket money. That’s where I was taught to sell, move and market fruit and I even negotiated with the buyers, he says. In 2003 Mansfield matriculated from Kylemore High school, an achievement he says wouldn’t have been possible without the support of his parents. After school I worked for my uncle for about six months and then my father gave me his small Nissan bakkie. I started with 63 boxes of white grapes that I got from a farm in Simondium, I’ll never forget it. Soon Mansfield built relationships with farmers in the surrounding towns, buying their fruit to sell at the Cape Town market. In 2006, this fruit hawker started picking lemons for sale at Fairview Wine and Cheese. We started out picking lemons and we always worked together as a family. We did well and after a few years we even bought a bigger bakkie and a trailer, he muses. During this time he met Donald Matton and had started dealing directly with Fairview to pick, package and sell their lemons. This is also when Matton started encouraging Mansfield to consider farming the lemons. I knew nothing about farming. I know a tree needs water, its gets sprayed but I didn’t know the finer details of what needed to happen when it comes to farming with lemons. In 2014 Mansfield needed no more convincing and started to farm seven hectares on Fairview. I started farming on land that hadn’t produced lemons in 7 or 8 years. Fairview had stopped farming on this specific piece of land, there was no water, no spraying or feeding of the trees. During this time Mansfield also met with Charles Back, owner of Fairview. We spoke and I told him about my plans to farm and that I’d apply for funding from the department of agriculture through their Comprehensive Agricultural Support Programme (CASP) funding. Fairview did so much, we could use the farm’s equipment and Back even paid the six people I employed. The agreement was that he would write up everything that I used and the day I got my first money from the overseas exports I should pay him back rent free. Within that first year of farming I paid him back and exported 31 tons of lemons. One year later Mansfield increased his lemon exports from 31 tons to 163 tons. When asked about how he managed to do this, Mansfield explains that when he started farming he asked his dominee (pastor or clergyman) to bless his farm, an important religious practice that Mansfield believes was key to his growth as a farmer. My success that year was not just me, there were a number of key role players and I can’t take the credit alone. Fairview was there for me, the department of agriculture and their team was there for me. During this time I learnt a lot from other farmers. I had a number of mentors in the area and I could call any one of them to ask questions. For this farmer, this is just the beginning. He plans to grow his business to generate enough capital to get to where he actually wants to be. “For now farming is good, and I won’t stop farming. Even if I start with other businesses, farming will always be my primary business. In the near future I would like to go bigger. Get something that I farm alongside the lemons to be active for 12 months of the year. Mansfield believes that the biggest hurdles in life are the ones you put there yourself. Staying disciplined, focused and humble is a big challenge for me. About seven years ago I started taking care of my parents, which was challenging, but I would do it all over again with love. This act of love is what he accredits his success to today. Often I’ll get things or achieve things, then I’ll wonder ‘but why me?’, because others don’t often get these opportunities. Mansfield, still aching from his father’s death last year, says his dad was very instrumental in his success. In 2018 Mansfield won Agricultural Writers SA’s 2018 Western Cape New Entrant Into Commercial Agriculture award. This was a great achievement. It was all the hard work we put in. I didn’t think I would be nominated after only three years. Looking to the future, Mansfield plans to grow his business to give back to people who may not have received the opportunities he has been given. In the same breath his aim is to produce more and better fruit and learn more about his growing business.",
        uploaded_at=datetime.utcnow(),
        processed=False
)

    # Add to the session and commit to the database
    db.session.add(new_uploaded_data)
    db.session.commit()

    print("Data added successfully!")