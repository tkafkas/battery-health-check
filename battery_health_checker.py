import psutil
import datetime
import subprocess
import os
import re
from bs4 import BeautifulSoup

def parse_battery_report(report_path):
    """Parse more detailed information from the battery report"""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find battery information table
        tables = soup.find_all('table')
        battery_info = {}
        
        # Process Battery Information table
        for table in tables:
            headers = [th.text.strip() for th in table.find_all('th')]
            if 'DESIGN CAPACITY' in str(table):
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        key = cols[0].text.strip()
                        value = cols[1].text.strip()
                        if 'DESIGN CAPACITY' in key:
                            battery_info['design_capacity'] = value.split()[0]  # Get the number only
                        elif 'FULL CHARGE CAPACITY' in key:
                            battery_info['full_charge_capacity'] = value.split()[0]  # Get the number only
                        elif 'CYCLE COUNT' in key:
                            battery_info['cycle_count'] = value
            
            # Get recent usage from Usage History table
            elif 'DURATION' in str(table):
                rows = table.find_all('tr')[1:]  # Skip header row
                recent_usage = []
                for row in rows[-3:]:  # Get last 3 entries
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        recent_usage.append([
                            cols[0].text.strip(),  # Start time
                            cols[1].text.strip(),  # Duration
                            cols[2].text.strip(),  # Active
                            cols[3].text.strip()   # Power
                        ])
                battery_info['recent_usage'] = recent_usage

        # Calculate battery wear level
        try:
            design_cap = int(battery_info.get('design_capacity', 0))
            full_cap = int(battery_info.get('full_charge_capacity', 0))
            if design_cap > 0 and full_cap > 0:
                battery_info['wear_level'] = round((1 - full_cap/design_cap) * 100, 2)
            else:
                battery_info['wear_level'] = "Unknown"
        except:
            battery_info['wear_level'] = "Unknown"
            
        return battery_info
    except Exception as e:
        print(f"Error parsing battery report: {str(e)}")  # Debug output
        return {"error": f"Could not parse battery report: {str(e)}"}

def generate_battery_report():
    """Generate Windows battery report"""
    try:
        report_path = os.path.join(os.getcwd(), "battery-report.html")
        subprocess.run(["powercfg", "/batteryreport", "/output", report_path], 
                      capture_output=True, text=True, check=True)
        return parse_battery_report(report_path)
    except Exception as e:
        return {"error": f"Could not generate battery report: {str(e)}"}

def format_duration(duration_str):
    """Format duration string to be more readable"""
    if ':' in duration_str:
        parts = duration_str.split(':')
        if len(parts) == 3:
            return f"{parts[0]}h {parts[1]}m {parts[2]}s"
    return duration_str

def check_battery():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery detected - device might be running on direct power supply"
        
        # Get battery percentage and power status
        percent = battery.percent
        power_plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
        
        # Calculate time remaining
        if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            if battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                time_left = str(datetime.timedelta(seconds=battery.secsleft))
            else:
                time_left = "Time remaining unknown"
        else:
            time_left = "Unlimited (Connected to power supply)"

        # Get detailed battery report
        report_info = generate_battery_report()
        
        # Create status message
        status = f"""
╔════════════════════════════════════════════════════════════════╗
║                    Battery Status Report                        ║
╠════════════════════════════════════════════════════════════════╣
║ Current Status:                                                ║
║ • Battery Level: {percent}%                                     {'║' if percent < 10 else '║'}
║ • Power Status: {power_plugged}                            {'║' if len(power_plugged) < 20 else '║'}
║ • Time Remaining: {time_left}                              {'║' if len(str(time_left)) < 20 else '║'}
╠════════════════════════════════════════════════════════════════╣
║ Battery Health Information:                                    ║
║ • Design Capacity: {report_info.get('design_capacity', 'Unknown')} mWh                           ║
║ • Current Capacity: {report_info.get('full_charge_capacity', 'Unknown')} mWh                         ║
║ • Cycle Count: {report_info.get('cycle_count', 'Unknown')}                                      ║
║ • Battery Wear: {report_info.get('wear_level', 'Unknown')}%                                     ║
╠════════════════════════════════════════════════════════════════╣
║ Health Indicators:                                             ║
║ • {'🔴 Critical' if percent < 10 else '🟡 Low' if percent < 20 else '🟢 Good'} Battery Level        ║
║ • {'🔴 High Wear' if isinstance(report_info.get('wear_level'), (int, float)) and report_info['wear_level'] > 30 else '🟡 Moderate Wear' if isinstance(report_info.get('wear_level'), (int, float)) and report_info['wear_level'] > 20 else '🟢 Normal Wear'}                                          ║
╠════════════════════════════════════════════════════════════════╣
║ Recent Usage Pattern (Last 3 Sessions):                        ║"""

        # Add recent usage if available
        if report_info.get('recent_usage'):
            for session in report_info['recent_usage']:
                if len(session) >= 4:
                    status += f"""
║ • {session[0][:10]}: Active {session[2]}, Power {session[3]}  ║"""
        else:
            status += """
║ • No recent usage data available                              ║"""

        status += """
╚════════════════════════════════════════════════════════════════╝

Note: A detailed HTML report has been generated as 'battery-report.html'
      Open this file in your web browser for complete historical data.
"""
        return status
    
    except Exception as e:
        return f"Error checking battery status: {str(e)}"

if __name__ == "__main__":
    print(check_battery())