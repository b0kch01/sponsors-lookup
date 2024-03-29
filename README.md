<div align=center>

<img src="readme/investigate.gif" width=75 height=75>
  
`
(me looking for campus recruiters)
`

<img width="544" src="https://github.com/b0kch01/sponsors-lookup/assets/44041512/3023f46d-52bc-4f1a-bfce-f04342242ce4">



# Sponsors Lookup
  
  ```
🔎 Quickly compile a list of sponsor contacts for your university hackathon!
```



</div>

## Example Ranking
<details>
<summary>Meta</summary>
  
|    | name              | title                     |   quality_score |
|---:|:------------------|:--------------------------|----------------:|
|  0 | Rebecca Ferrara   | Technical Recruiter       |            1070 |
|  1 | Long H            | Sourcing Manager          |            1045 |
|  2 | Kristen J         | Recruiting Leader         |            1040 |
|  3 | Scott Steinhauser | Software Engineer         |            1000 |

</details>

<details>
<summary>Twilio</summary>
  
|    | name                | title                                           |   quality_score |
|---:|:--------------------|:------------------------------------------------|----------------:|
|  0 | Lizzie Siegle       | Developer Evangelist Lll                        |            1500 |
|  1 | Aaron Tran          | Technical Recruiter                             |            1070 |
|  2 | Halley McCormack    | Senior Technical Recruiter III                  |            1060 |
|  3 | Monty Gill          | Senior Talent Partner, R&D Technical Leadership |            1060 |
|  4 | Anthony Spangenberg | Staff Data Analyst, Talent Acquisition          |            1050 |

</details>

<details>
<summary>Crowdstrike</summary>
  
|    | name         | title                                  |   quality_score |
|---:|:-------------|:---------------------------------------|----------------:|
|  0 | Anna Schuh   | University Campus Recruiter            |            1150 |
|  1 | Monica Ipong | Director, Global University Recruiting |            1140 |
|  2 | Larry Young  | Senior Technical Recruiter             |            1060 |
|  3 | Abe Ramos    | Senior Technical Recruiter             |            1060 |
|  4 | Mina Sarshar | Recruiter                              |            1050 |

</details>


## Instructions



1. Clone this repo
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the script using Python 3 (Tested on 3.11)
```bash
python3 main.py
``` 

### Turbo Mode Setup
1. Create a file called `existing.txt` in the `input/` directory
2. Add the emails of the companies you already contacted/found in the file
3. Create a file called `new.txt` in the `input/` directory
4. Add the emails of the companies you want to analyze in the file
 - The script will automatically remove duplicates


## Progress
- [ ] Smarter company tagging
- [X] Store results and allow for easy copy-n-paste
  - [X] Single-row copy
  - [X] Multi-row copy with input_file
- [X] Reverse engineer email lookup feature
  - [X] Implement into API
- [x] Employee selection algorithm
- [x] Company selection algorithm

## Related Tools for Organizers
> 🚩 Flags GitHub projects with low commit numbers and unprofessional code.
> https://github.com/b0kch01/JudgeJudy
