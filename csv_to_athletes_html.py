import csv
import os
import glob

def generate_nav_html(directory):
    links = []

    # Homepage link
    homepage_link = '<a href="../index.html">Homepage</a>'
    links.append(homepage_link)

    # Generate links for each HTML file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            link = f'<a href="{filename}">{filename.replace(".html", "")}</a>'
            links.append(link)

    links_html = "<br>\n".join(links)
    nav_html = f'<nav class="roster-nav"><details id="roster"><summary>Men\'s Roster</summary>\n{links_html}\n</details></nav>'

    return nav_html

# Get current working directory and generate navigation HTML
dir = os.getcwd()
nav_html_content = generate_nav_html(dir + "/mens_team")

def process_athlete_data(file_path):
    records = []  # Extracting athlete stats by year
    races = []    # Extracting athlete races
    athlete_name = ""
    athlete_id = ""

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

        # Read athlete's name and ID
        athlete_name = data[0][0]
        athlete_id = data[1][0]
        print(f"The athlete ID for {athlete_name} is {athlete_id}")

        # Process data starting from the 6th row
        for row in data[5:-1]:
            if row[2]:  # If there's a season record
                records.append({"year": row[2], "sr": row[3]})
            else:  # Otherwise, it's a race result
                races.append({
                    "finish": row[1],
                    "time": row[3],
                    "meet": row[5],
                    "url": row[6],
                    "comments": row[7]
                })

    return {
        "name": athlete_name,
        "athlete_id": athlete_id,
        "season_records": records,
        "race_results": races
    }

def gen_athlete_page(data, outfile):
    athlete_image_path = f"profiles/{data['athlete_id']}"

    # Start building the HTML structure
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Get your own FontAwesome ID -->
    <script src="https://kit.fontawesome.com/b3d61a60b3.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="../css/style.css">
    <title>{data["name"]}</title>
</head>
<body>
    <a href="#main" class="skip">Skip to Main Content</a>
    <div class="content-wrapper">
    {nav_html_content}
    <div class="header-main-wrapper">
    <header>
        <h1>{data["name"]}</h1>
        <img src="../images/{athlete_image_path}.jpg" id="profileImage" class="profile-image" alt="Athlete headshot" onerror="this.onerror=null; this.src='../images/profiles/default_image.jpg'">
    </header>
    <main id="main">
        <section id="athlete-sr-table">
            <h2>Athlete's Seasonal Records (SR) per Year</h2>
            <table>
                <thead>
                    <tr>
                        <th>Year</th>
                        <th>Season Record (SR)</th>
                    </tr>
                </thead>
                <tbody>
    '''

    # Add each seasonal record as a row in the table
    for sr in data["season_records"]:
        sr_row = f'''
                    <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                    </tr>
        '''
        html_content += sr_row

    html_content += '''
                </tbody>
            </table>
        </section>

        <h2>Race Results</h2>
        <details id="race-results">
            <summary>Click to expand Race Results</summary>
            <section id="athlete-result-table">
                <table id="athlete-table">
                    <thead>
                        <tr>
                            <th>Race</th>
                            <th>Athlete Time</th>
                            <th>Athlete Place</th>
                            <th>Race Comments</th>
                        </tr>
                    </thead>
                    <tbody>
    '''

    # Add each race as a row in the race table
    for race in data["race_results"]:
        race_row = f'''
                    <tr class="result-row">
                        <td><a href="{race["url"]}">{race["meet"]}</a></td>
                        <td>{race["time"]}</td>
                        <td>{race["finish"]}</td>
                        <td>{race["comments"]}</td>
                    </tr>
        '''
        html_content += race_row

    html_content += '''
                    </tbody>
                </table>
            </section>
        </details>
    </main>
    <br><br>
    </div>
    </div>
    <footer>
        <address>
        <p>Skyline High School<br>
            2552 North Maple Road<br>
            Ann Arbor, MI 48103<br><br>
            <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
            <a href="https://www.instagram.com/a2skylinexc/" target="_blank" rel="noopener noreferrer" aria-label="Follow us on Instagram">
                Follow us on Instagram <i class="fab fa-instagram" aria-hidden="true"></i>
            </a>
        </p>
        </address>
    </footer>
    <script src="../js/script.js"></script>
</body>
</html>
'''

    # Write the generated HTML content to the output file
    with open(outfile, 'w') as output:
        output.write(html_content)

def main():
    # Process men's team CSV files
    folder_path = 'mens_team/'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Output the list of CSV file names
    print([os.path.basename(file) for file in csv_files])

    for file in csv_files:
        athlete_data = process_athlete_data(file)
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

    # Process women's team CSV files
    folder_path = 'womens_team/'
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Output the list of CSV file names
    print([os.path.basename(file) for file in csv_files])

    for file in csv_files:
        athlete_data = process_athlete_data(file)
        gen_athlete_page(athlete_data, file.replace(".csv", ".html"))

if __name__ == '__main__':
    main()
