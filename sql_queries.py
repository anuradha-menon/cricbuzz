QUERIES = [
    # Beginner Level (Questions 1-8)
    {
        "level": "Beginner",
        "id": 1,
        "question": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "sql": """
        SELECT full_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country = 'India';
        """
    },
    {
        "level": "Beginner",
        "id": 2,
        "question": "Show all cricket matches that were played in the last 30 days. Include the match description, both team names, venue name with city, and the match date. Sort by most recent matches first.",
        "sql": """
        SELECT m.description, m.team1, m.team2, v.name || ', ' || v.city AS venue, m.match_date
        FROM matches m
        JOIN venues v ON m.venue_id = v.id
        WHERE m.match_date >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY m.match_date DESC;
        """
    },
    {
        "level": "Beginner",
        "id": 3,
        "question": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first.",
        "sql": """
        SELECT full_name, odi_runs AS total_runs, odi_avg AS batting_average, odi_centuries AS centuries
        FROM players
        WHERE odi_runs > 0
        ORDER BY odi_runs DESC
        LIMIT 10;
        """
    },
    {
        "level": "Beginner",
        "id": 4,
        "question": "Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.",
        "sql": """
        SELECT name, city, country, capacity
        FROM venues
        WHERE capacity > 50000
        ORDER BY capacity DESC;
        """
    },
    {
        "level": "Beginner",
        "id": 5,
        "question": "Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.",
        "sql": """
        SELECT winner AS team_name, COUNT(*) AS total_wins
        FROM matches
        GROUP BY winner
        ORDER BY total_wins DESC;
        """
    },
    {
        "level": "Beginner",
        "id": 6,
        "question": "Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.",
        "sql": """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        GROUP BY playing_role;
        """
    },
    {
        "level": "Beginner",
        "id": 7,
        "question": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display the format and the highest score for that format.",
        "sql": """
        SELECT 'ODI' AS format, MAX(odi_highest_score) AS highest_score FROM players
        UNION ALL
        SELECT 'Test' AS format, MAX(test_highest_score) AS highest_score FROM players
        UNION ALL
        SELECT 'T20I' AS format, MAX(t20_highest_score) AS highest_score FROM players;
        """  # Note: Add columns like odi_highest_score to schema if needed
    },
    {
        "level": "Beginner",
        "id": 8,
        "question": "Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.",
        "sql": """
        SELECT name AS series_name, host_country, match_type, start_date, total_matches
        FROM series
        WHERE EXTRACT(YEAR FROM start_date) = 2024;
        """
    },

    # Intermediate Level (Questions 9-16)
    {
        "level": "Intermediate",
        "id": 9,
        "question": "Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name, total runs, total wickets, and the cricket format.",
        "sql": """
        SELECT full_name, odi_runs AS total_runs, odi_wickets AS total_wickets, 'ODI' AS format
        FROM players
        WHERE playing_role = 'All-rounder' AND odi_runs > 1000 AND odi_wickets > 50
        UNION ALL
        SELECT full_name, test_runs AS total_runs, test_wickets AS total_wickets, 'Test' AS format
        FROM players
        WHERE playing_role = 'All-rounder' AND test_runs > 1000 AND test_wickets > 50
        UNION ALL
        SELECT full_name, t20_runs AS total_runs, t20_wickets AS total_wickets, 'T20I' AS format
        FROM players
        WHERE playing_role = 'All-rounder' AND t20_runs > 1000 AND t20_wickets > 50;
        """
    },
    {
        "level": "Intermediate",
        "id": 10,
        "question": "Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.",
        "sql": """
        SELECT m.description, m.team1, m.team2, m.winner, m.victory_margin, m.victory_type, v.name AS venue
        FROM matches m
        JOIN venues v ON m.venue_id = v.id
        WHERE m.winner IS NOT NULL
        ORDER BY m.match_date DESC
        LIMIT 20;
        """
    },
    {
        "level": "Intermediate",
        "id": 11,
        "question": "Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test cricket, ODI cricket, and T20I cricket, along with their overall batting average across all formats.",
        "sql": """
        WITH format_counts AS (
            SELECT full_name,
                   CASE WHEN test_runs > 0 THEN 1 ELSE 0 END +
                   CASE WHEN odi_runs > 0 THEN 1 ELSE 0 END +
                   CASE WHEN t20_runs > 0 THEN 1 ELSE 0 END AS formats_played
            FROM players
        )
        SELECT p.full_name, p.test_runs, p.odi_runs, p.t20_runs,
               COALESCE((p.test_avg + p.odi_avg + p.t20_avg) / NULLIF((CASE WHEN p.test_runs > 0 THEN 1 ELSE 0 END + CASE WHEN p.odi_runs > 0 THEN 1 ELSE 0 END + CASE WHEN p.t20_runs > 0 THEN 1 ELSE 0 END), 0), 0) AS overall_avg
        FROM players p
        JOIN format_counts fc ON p.full_name = fc.full_name
        WHERE fc.formats_played >= 2;
        """
    },
    {
        "level": "Intermediate",
        "id": 12,
        "question": "Analyze each international team's performance when playing at home versus playing away. Determine whether each team played at home or away based on whether the venue country matches the team's country. Count wins for each team in both home and away conditions.",
        "sql": """
        WITH team_performance AS (
            SELECT m.winner AS team, v.country AS venue_country,
                   CASE WHEN v.country = (SELECT country FROM players WHERE country = m.team1 LIMIT 1) THEN 'Home' ELSE 'Away' END AS condition
            FROM matches m
            JOIN venues v ON m.venue_id = v.id
            WHERE m.winner IS NOT NULL
        )
        SELECT team, condition, COUNT(*) AS wins
        FROM team_performance
        GROUP BY team, condition
        ORDER BY team, condition;
        """
    },
    {
        "level": "Intermediate",
        "id": 13,
        "question": "Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings. Show both player names, their combined partnership runs, and which innings it occurred in.",
        "sql": """
        SELECT bp1.player_id AS player1, bp2.player_id AS player2, bp1.runs + bp2.runs AS partnership_runs, bp1.innings_num
        FROM batting_performances bp1
        JOIN batting_performances bp2 ON bp1.match_id = bp2.match_id AND bp1.innings_num = bp2.innings_num AND ABS(bp1.position - bp2.position) = 1
        WHERE bp1.runs + bp2.runs >= 100;
        """
    },
    {
        "level": "Intermediate",
        "id": 14,
        "question": "Examine bowling performance at different venues. For bowlers who have played at least 3 matches at the same venue, calculate their average economy rate, total wickets taken, and number of matches played at each venue. Focus on bowlers who bowled at least 4 overs in each match.",
        "sql": """
        SELECT p.full_name, v.name AS venue, AVG(bp.economy_rate) AS avg_economy, SUM(bp.wickets) AS total_wickets, COUNT(bp.match_id) AS matches_played
        FROM bowling_performances bp
        JOIN players p ON bp.player_id = p.id
        JOIN venues v ON bp.venue_id = v.id
        WHERE bp.overs >= 4
        GROUP BY p.full_name, v.name
        HAVING COUNT(bp.match_id) >= 3;
        """
    },
    {
        "level": "Intermediate",
        "id": 15,
        "question": "Identify players who perform exceptionally well in close matches. A close match is defined as one decided by less than 50 runs OR less than 5 wickets. For these close matches, calculate each player's average runs scored, total close matches played, and how many of those close matches their team won when they batted.",
        "sql": """
        WITH close_matches AS (
            SELECT id
            FROM matches
            WHERE (victory_type = 'runs' AND victory_margin < 50) OR (victory_type = 'wickets' AND victory_margin < 5)
        )
        SELECT p.full_name, AVG(bp.runs) AS avg_runs, COUNT(bp.match_id) AS close_matches_played, SUM(CASE WHEN m.winner = bp.team WHEN 1 ELSE 0 END) AS team_wins
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.id
        JOIN matches m ON bp.match_id = m.id
        JOIN close_matches cm ON m.id = cm.id
        GROUP BY p.full_name;
        """
    },
    {
        "level": "Intermediate",
        "id": 16,
        "question": "Track how players' batting performance changes over different years. For matches since 2020, show each player's average runs per match and average strike rate for each year. Only include players who played at least 5 matches in that year.",
        "sql": """
        SELECT p.full_name, EXTRACT(YEAR FROM m.match_date) AS year, AVG(bp.runs) AS avg_runs_per_match, AVG(bp.strike_rate) AS avg_strike_rate
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.id
        JOIN matches m ON bp.match_id = m.id
        WHERE m.match_date >= '2020-01-01'
        GROUP BY p.full_name, year
        HAVING COUNT(bp.match_id) >= 5
        ORDER BY p.full_name, year;
        """
    },

    # Advanced Level (Questions 17-25)
    {
        "level": "Advanced",
        "id": 17,
        "question": "Investigate whether winning the toss gives teams an advantage in winning matches. Calculate what percentage of matches are won by the team that wins the toss, broken down by their toss decision (choosing to bat first or bowl first).",
        "sql": """
        WITH toss_wins AS (
            SELECT toss_decision, COUNT(*) AS toss_win_count, SUM(CASE WHEN winner = toss_winner THEN 1 ELSE 0 END) AS match_wins
            FROM matches
            WHERE toss_winner IS NOT NULL
            GROUP BY toss_decision
        )
        SELECT toss_decision, (match_wins * 100.0 / toss_win_count) AS win_percentage
        FROM toss_wins;
        """
    },
    {
        "level": "Advanced",
        "id": 18,
        "question": "Find the most economical bowlers in limited-overs cricket (ODI and T20 formats). Calculate each bowler's overall economy rate and total wickets taken. Only consider bowlers who have bowled in at least 10 matches and bowled at least 2 overs per match on average.",
        "sql": """
        SELECT p.full_name, AVG(bp.economy_rate) AS overall_economy, SUM(bp.wickets) AS total_wickets
        FROM bowling_performances bp
        JOIN players p ON bp.player_id = p.id
        JOIN matches m ON bp.match_id = m.id
        WHERE m.format IN ('ODI', 'T20I')
        GROUP BY p.full_name
        HAVING COUNT(bp.match_id) >= 10 AND AVG(bp.overs) >= 2
        ORDER BY overall_economy ASC;
        """
    },
    {
        "level": "Advanced",
        "id": 19,
        "question": "Determine which batsmen are most consistent in their scoring. Calculate the average runs scored and the standard deviation of runs for each player. Only include players who have faced at least 10 balls per innings and played since 2022. A lower standard deviation indicates more consistent performance.",
        "sql": """
        SELECT p.full_name, AVG(bp.runs) AS avg_runs, STDDEV(bp.runs) AS stddev_runs
        FROM batting_performances bp
        JOIN players p ON bp.player_id = p.id
        JOIN matches m ON bp.match_id = m.id
        WHERE bp.balls >= 10 AND m.match_date >= '2022-01-01'
        GROUP BY p.full_name
        ORDER BY stddev_runs ASC;
        """
    },
    {
        "level": "Advanced",
        "id": 20,
        "question": "Analyze how many matches each player has played in different cricket formats and their batting average in each format. Show the count of Test matches, ODI matches, and T20 matches for each player, along with their respective batting averages. Only include players who have played at least 20 total matches across all formats.",
        "sql": """
        WITH format_stats AS (
            SELECT p.full_name,
                   SUM(CASE WHEN m.format = 'Test' THEN 1 ELSE 0 END) AS test_matches,
                   AVG(CASE WHEN m.format = 'Test' THEN p.test_avg ELSE NULL END) AS test_avg,
                   SUM(CASE WHEN m.format = 'ODI' THEN 1 ELSE 0 END) AS odi_matches,
                   AVG(CASE WHEN m.format = 'ODI' THEN p.odi_avg ELSE NULL END) AS odi_avg,
                   SUM(CASE WHEN m.format = 'T20I' THEN 1 ELSE 0 END) AS t20_matches,
                   AVG(CASE WHEN m.format = 'T20I' THEN p.t20_avg ELSE NULL END) AS t20_avg
            FROM players p
            JOIN batting_performances bp ON p.id = bp.player_id
            JOIN matches m ON bp.match_id = m.id
            GROUP BY p.full_name
        )
        SELECT full_name, test_matches, odi_matches, t20_matches, test_avg, odi_avg, t20_avg
        FROM format_stats
        WHERE test_matches + odi_matches + t20_matches >= 20;
        """
    },
    {
        "level": "Advanced",
        "id": 21,
        "question": "Create a comprehensive performance ranking system for players. Combine their batting performance (runs scored, batting average, strike rate), bowling performance (wickets taken, bowling average, economy rate), and fielding performance (catches, stumpings) into a single weighted score. Use this formula and rank players: Batting points: (runs_scored × 0.01) + (batting_average × 0.5) + (strike_rate × 0.3) Bowling points: (wickets_taken × 2) + (50 - bowling_average) × 0.5) + ((6 - economy_rate) × 2) Fielding points: (catches × 3) + (stumpings × 5) Rank the top performers in each cricket format.",
        "sql": """
        WITH ranking AS (
            SELECT full_name, format,
                   (runs_scored * 0.01 + batting_average * 0.5 + strike_rate * 0.3) + (wickets_taken * 2 + (50 - bowling_average) * 0.5 + (6 - economy_rate) * 2) + (catches * 3 + stumpings * 5) AS score
            FROM (
                SELECT full_name, 'ODI' AS format, odi_runs AS runs_scored, odi_avg AS batting_average, strike_rate, odi_wickets AS wickets_taken, odi_bowling_avg AS bowling_average, economy_rate, catches, stumpings
                FROM players
                UNION ALL
                SELECT full_name, 'Test' AS format, test_runs AS runs_scored, test_avg AS batting_average, strike_rate, test_wickets AS wickets_taken, test_bowling_avg AS bowling_average, economy_rate, catches, stumpings
                FROM players
                UNION ALL
                SELECT full_name, 'T20I' AS format, t20_runs AS runs_scored, t20_avg AS batting_average, strike_rate, t20_wickets AS wickets_taken, t20_bowling_avg AS bowling_average, economy_rate, catches, stumpings
                FROM players
            ) AS all_formats
            WHERE runs_scored > 0 OR wickets_taken > 0
        )
        SELECT full_name, format, score, RANK() OVER (PARTITION BY format ORDER BY score DESC) AS rank
        FROM ranking
        ORDER BY format, rank;
        """  # Note: Add missing columns like odi_bowling_avg to schema if needed
    },
    {
        "level": "Advanced",
        "id": 22,
        "question": "Build a head-to-head match prediction analysis between teams. For each pair of teams that have played at least 5 matches against each other in the last 3 years, calculate: Total matches played between them, Wins for each team, Average victory margin when each team wins, Performance when batting first vs bowling first at different venues, Overall win percentage for each team in this head-to-head record.",
        "sql": """
        WITH h2h AS (
            SELECT LEAST(team1, team2) AS team_a, GREATEST(team1, team2) AS team_b, COUNT(*) AS total_matches,
                   SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) AS team1_wins,
                   SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) AS team2_wins,
                   AVG(CASE WHEN winner = team1 THEN victory_margin ELSE NULL END) AS team1_avg_margin,
                   AVG(CASE WHEN winner = team2 THEN victory_margin ELSE NULL END) AS team2_avg_margin,
                   SUM(CASE WHEN toss_decision = 'bat' AND winner = toss_winner THEN 1 ELSE 0 END) AS bat_first_wins,
                   SUM(CASE WHEN toss_decision = 'bowl' AND winner = toss_winner THEN 1 ELSE 0 END) AS bowl_first_wins
            FROM matches
            WHERE match_date >= CURRENT_DATE - INTERVAL '3 years'
            GROUP BY team_a, team_b
            HAVING COUNT(*) >= 5
        )
        SELECT team_a, team_b, total_matches, team1_wins, team2_wins, team1_avg_margin, team2_avg_margin, bat_first_wins, bowl_first_wins,
               (team1_wins * 100.0 / total_matches) AS team1_win_pct, (team2_wins * 100.0 / total_matches) AS team2_win_pct
        FROM h2h;
        """
    },
    {
        "level": "Advanced",
        "id": 23,
        "question": "Analyze recent player form and momentum. For each player's last 10 batting performances, calculate: Average runs in their last 5 matches vs their last 10 matches, Recent strike rate trends, Number of scores above 50 in recent matches, A consistency score based on standard deviation. Based on these metrics, categorize players as being in 'Excellent Form', 'Good Form', 'Average Form', or 'Poor Form'.",
        "sql": """
        WITH recent_batting AS (
            SELECT p.full_name, bp.runs, bp.strike_rate, bp.match_id,
                   ROW_NUMBER() OVER (PARTITION BY p.full_name ORDER BY m.match_date DESC) AS rank
            FROM batting_performances bp
            JOIN players p ON bp.player_id = p.id
            JOIN matches m ON bp.match_id = m.id
        ),
        form_stats AS (
            SELECT full_name,
                   AVG(CASE WHEN rank <= 5 THEN runs ELSE NULL END) AS avg_last5,
                   AVG(CASE WHEN rank <= 10 THEN runs ELSE NULL END) AS avg_last10,
                   AVG(CASE WHEN rank <= 10 THEN strike_rate ELSE NULL END) AS recent_strike_rate,
                   SUM(CASE WHEN rank <= 10 AND runs > 50 THEN 1 ELSE 0 END) AS scores_above50,
                   STDDEV(CASE WHEN rank <= 10 THEN runs ELSE NULL END) AS consistency_stddev
            FROM recent_batting
            GROUP BY full_name
            HAVING COUNT(*) >= 10
        )
        SELECT full_name, avg_last5, avg_last10, recent_strike_rate, scores_above50, consistency_stddev,
               CASE
                   WHEN avg_last5 > 40 AND consistency_stddev < 20 AND scores_above50 > 4 THEN 'Excellent Form'
                   WHEN avg_last5 > 30 AND consistency_stddev < 30 AND scores_above50 > 2 THEN 'Good Form'
                   WHEN avg_last5 > 20 THEN 'Average Form'
                   ELSE 'Poor Form'
               END AS form_category
        FROM form_stats;
        """
    },
    {
        "level": "Advanced",
        "id": 24,
        "question": "Study successful batting partnerships to identify the best player combinations. For pairs of players who have batted together as consecutive batsmen (positions differ by 1) in at least 5 partnerships: Calculate their average partnership runs, Count how many of their partnerships exceeded 50 runs, Find their highest partnership score, Calculate their success rate (percentage of good partnerships), Rank the most successful batting partnerships.",
        "sql": """
        WITH partnerships AS (
            SELECT LEAST(bp1.player_id, bp2.player_id) AS player1, GREATEST(bp1.player_id, bp2.player_id) AS player2,
                   bp1.runs + bp2.runs AS partnership_runs
            FROM batting_performances bp1
            JOIN batting_performances bp2 ON bp1.match_id = bp2.match_id AND bp1.innings_num = bp2.innings_num AND ABS(bp1.position - bp2.position) = 1
        )
        SELECT p1.full_name AS player1, p2.full_name AS player2, AVG(partnership_runs) AS avg_partnership, COUNT(*) AS total_partnerships,
               SUM(CASE WHEN partnership_runs > 50 THEN 1 ELSE 0 END) AS above50, MAX(partnership_runs) AS highest,
               (SUM(CASE WHEN partnership_runs > 50 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS success_rate
        FROM partnerships pr
        JOIN players p1 ON pr.player1 = p1.id
        JOIN players p2 ON pr.player2 = p2.id
        GROUP BY p1.full_name, p2.full_name
        HAVING COUNT(*) >= 5
        ORDER BY success_rate DESC;
        """
    },
    {
        "level": "Advanced",
        "id": 25,
        "question": "Perform a time-series analysis of player performance evolution. Track how each player's batting performance changes over time by: Calculating quarterly averages for runs and strike rate, Comparing each quarter's performance to the previous quarter, Identifying whether performance is improving, declining, or stable, Determining overall career trajectory over the last few years, Categorizing players' career phase as 'Career Ascending', 'Career Declining', or 'Career Stable'. Only analyze players with data spanning at least 6 quarters and a minimum of 3 matches per quarter.",
        "sql": """
        WITH quarterly_stats AS (
            SELECT p.full_name, EXTRACT(YEAR FROM m.match_date) || '-Q' || EXTRACT(QUARTER FROM m.match_date) AS quarter,
                   AVG(bp.runs) AS avg_runs, AVG(bp.strike_rate) AS avg_strike_rate, COUNT(bp.match_id) AS matches_played,
                   ROW_NUMBER() OVER (PARTITION BY p.full_name ORDER BY EXTRACT(YEAR FROM m.match_date) * 4 + EXTRACT(QUARTER FROM m.match_date)) AS q_rank
            FROM batting_performances bp
            JOIN players p ON bp.player_id = p.id
            JOIN matches m ON bp.match_id = m.id
            GROUP BY p.full_name, quarter
            HAVING COUNT(bp.match_id) >= 3
        ),
        trajectory AS (
            SELECT qs1.full_name, qs1.quarter, qs1.avg_runs, qs1.avg_strike_rate,
                   CASE WHEN qs1.avg_runs > qs2.avg_runs THEN 'Improving' WHEN qs1.avg_runs < qs2.avg_runs THEN 'Declining' ELSE 'Stable' END AS trend
            FROM quarterly_stats qs1
            LEFT JOIN quarterly_stats qs2 ON qs1.full_name = qs2.full_name AND qs1.q_rank = qs2.q_rank + 1
        ),
        overall_trend AS (
            SELECT full_name, STRING_AGG(trend, ', ') AS trends
            FROM trajectory
            GROUP BY full_name
            HAVING COUNT(*) >= 6
        )
        SELECT full_name,
               CASE
                   WHEN trends LIKE '%Improving%' AND trends NOT LIKE '%Declining%' THEN 'Career Ascending'
                   WHEN trends LIKE '%Declining%' AND trends NOT LIKE '%Improving%' THEN 'Career Declining'
                   ELSE 'Career Stable'
               END AS career_phase
        FROM overall_trend;
        """
    }
]