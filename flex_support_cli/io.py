import csv

def create_report(reportType, sid, data):
    filename = f"{reportType}-{sid}-report.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            if(reportType == "worker"):
                writer.writerow([
                     "Date Created", 
                     "Worker SID", 
                     "Friendly Name", 
                     "Activity Name", 
                     "Date Status Changed" 
                    ])
                for item in data:
                    print(f"Writing {item.sid} to {filename}")
                    writer.writerow([
                        item.date_created,
                        item.sid,
                        item.friendly_name,
                        item.activity_name,
                        item.date_status_changed
                    ])
            elif(reportType == "queue"):
                writer.writerow([
                    "Date Created", 
                    "Queue SID", 
                    "Friendly Name", 
                    "Target Workers", 
                    "Date Status Changed"
                ])
                for item in data:
                    writer.writerow([
                        item.date_created,
                        item.sid,
                        item.friendly_name,
                        item.target_workers
                    ])
            else:
                 print("Still Implementing this report type")
            
            return filename