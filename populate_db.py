from utils.db_connection import execute_query

# Clear existing data to avoid duplicates (optional, but recommended for testing)
execute_query("TRUNCATE TABLE players, matches, venues, series, batting_performances, bowling_performances RESTART IDENTITY")

# Insert players (4 players with multi-format stats)
execute_query("""
    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, odi_runs, odi_avg, odi_centuries, test_runs, test_avg, t20_runs, t20_avg, odi_wickets, test_wickets, t20_wickets, catches, stumpings, odi_highest_score, test_highest_score, t20_highest_score, odi_bowling_avg, test_bowling_avg, t20_bowling_avg)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('Virat Kohli', 'Batsman', 'Right-hand bat', 'Right-arm medium', 'India', 13000, 58.0, 46, 8000, 55.0, 4000, 40.0, 5, 0, 4, 150, 0, 254, 200, 122, 0, 0, 0))
execute_query("""
    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, odi_runs, odi_avg, odi_centuries, test_runs, test_avg, t20_runs, t20_avg, odi_wickets, test_wickets, t20_wickets, catches, stumpings, odi_highest_score, test_highest_score, t20_highest_score, odi_bowling_avg, test_bowling_avg, t20_bowling_avg)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('Joe Root', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'England', 6000, 50.0, 16, 12000, 50.0, 2000, 35.0, 20, 50, 10, 100, 0, 150, 254, 90, 40.0, 35.0, 30.0))
execute_query("""
    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, odi_runs, odi_avg, odi_centuries, test_runs, test_avg, t20_runs, t20_avg, odi_wickets, test_wickets, t20_wickets, catches, stumpings, odi_highest_score, test_highest_score, t20_highest_score, odi_bowling_avg, test_bowling_avg, t20_bowling_avg)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('Rohit Sharma', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'India', 10000, 48.0, 30, 4000, 45.0, 3000, 38.0, 8, 0, 7, 120, 0, 264, 212, 118, 0, 0, 0))
execute_query("""
    INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, odi_runs, odi_avg, odi_centuries, test_runs, test_avg, t20_runs, t20_avg, odi_wickets, test_wickets, t20_wickets, catches, stumpings, odi_highest_score, test_highest_score, t20_highest_score, odi_bowling_avg, test_bowling_avg, t20_bowling_avg)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('Jasprit Bumrah', 'Bowler', 'Right-hand bat', 'Right-arm fast', 'India', 100, 10.0, 0, 200, 8.0, 50, 5.0, 150, 200, 70, 50, 0, 30, 50, 20, 25.0, 20.0, 22.0))

# Insert venues (3 venues)
execute_query("""
    INSERT INTO venues (name, city, country, capacity)
    VALUES (%s, %s, %s, %s)
""", ('Eden Gardens', 'Kolkata', 'India', 66000))
execute_query("""
    INSERT INTO venues (name, city, country, capacity)
    VALUES (%s, %s, %s, %s)
""", ('Lord''s', 'London', 'England', 30000))
execute_query("""
    INSERT INTO venues (name, city, country, capacity)
    VALUES (%s, %s, %s, %s)
""", ('MCG', 'Melbourne', 'Australia', 90000))

# Insert series (2 series)
execute_query("""
    INSERT INTO series (name, host_country, match_type, start_date, total_matches)
    VALUES (%s, %s, %s, %s, %s)
""", ('India Tour of England 2024', 'England', 'ODI', '2024-01-01', 5))
execute_query("""
    INSERT INTO series (name, host_country, match_type, start_date, total_matches)
    VALUES (%s, %s, %s, %s, %s)
""", ('Ashes 2023', 'Australia', 'Test', '2023-12-01', 5))

# Insert matches (3 matches)
execute_query("""
    INSERT INTO matches (description, team1, team2, venue_id, match_date, format, winner, victory_margin, victory_type, toss_winner, toss_decision)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('India vs England 1st ODI', 'India', 'England', 1, '2024-01-10', 'ODI', 'India', 50, 'runs', 'India', 'bat'))
execute_query("""
    INSERT INTO matches (description, team1, team2, venue_id, match_date, format, winner, victory_margin, victory_type, toss_winner, toss_decision)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('India vs England 2nd ODI', 'India', 'England', 2, '2024-01-15', 'ODI', 'England', 4, 'wickets', 'England', 'bowl'))
execute_query("""
    INSERT INTO matches (description, team1, team2, venue_id, match_date, format, winner, victory_margin, victory_type, toss_winner, toss_decision)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", ('Australia vs England 1st Test', 'Australia', 'England', 3, '2023-12-05', 'Test', 'Australia', 200, 'runs', 'Australia', 'bat'))

# Insert batting performances (4 performances)
execute_query("""
    INSERT INTO batting_performances (match_id, player_id, innings_num, position, runs, balls, strike_rate, year, team)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (1, 1, 1, 3, 100, 120, 83.33, 2024, 'India'))  # Kohli in 1st ODI
execute_query("""
    INSERT INTO batting_performances (match_id, player_id, innings_num, position, runs, balls, strike_rate, year, team)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (1, 3, 1, 1, 80, 90, 88.89, 2024, 'India'))  # Rohit in 1st ODI
execute_query("""
    INSERT INTO batting_performances (match_id, player_id, innings_num, position, runs, balls, strike_rate, year, team)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (2, 2, 2, 4, 120, 100, 120.0, 2024, 'England'))  # Root in 2nd ODI
execute_query("""
    INSERT INTO batting_performances (match_id, player_id, innings_num, position, runs, balls, strike_rate, year, team)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (3, 2, 1, 4, 200, 300, 66.67, 2023, 'England'))  # Root in Test

# Insert bowling performances (3 performances)
execute_query("""
    INSERT INTO bowling_performances (match_id, player_id, overs, wickets, economy_rate, venue_id)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (1, 4, 10.0, 3, 4.5, 1))  # Bumrah in 1st ODI
execute_query("""
    INSERT INTO bowling_performances (match_id, player_id, overs, wickets, economy_rate, venue_id)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (2, 4, 8.0, 2, 5.0, 2))  # Bumrah in 2nd ODI
execute_query("""
    INSERT INTO bowling_performances (match_id, player_id, overs, wickets, economy_rate, venue_id)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (3, 4, 20.0, 5, 3.5, 3))  # Bumrah in Test

print("Sample data added")