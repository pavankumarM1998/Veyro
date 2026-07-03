import os
import json
from fastapi import FastAPI, Request, Form
from typing import Optional
from fastapi.templating import Jinja2Templates
from connection import send_to_event_hub, generate_veyro_ride_confirmation

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def save_booking_locally(ride_data):
    filepath = os.path.join("Data", "local_bookings.json")
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Load existing data
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
            
        data.append(ride_data)
        
        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving booking locally: {e}")


@app.get("/")
def booking_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/book")
def book_form(request: Request):
    return templates.TemplateResponse("book.html", {"request": request})


@app.post("/book")
def process_booking(
    request: Request,
    passenger_name: Optional[str] = Form(None),
    pickup_address: Optional[str] = Form(None),
    dropoff_address: Optional[str] = Form(None),
    vehicle_type: Optional[str] = Form(None),
    payment_method: Optional[str] = Form(None)
):  
    ride = generate_veyro_ride_confirmation(
        custom_pickup=pickup_address if pickup_address else None,
        custom_dropoff=dropoff_address if dropoff_address else None,
        custom_passenger_name=passenger_name if passenger_name else None,
        custom_vehicle_type=vehicle_type if vehicle_type else None,
        custom_payment_method=payment_method if payment_method else None
    )
    result = send_to_event_hub(ride)
    
    # Save booking locally (non-blocking for existing functionality)
    save_booking_locally(ride)
    
    return templates.TemplateResponse("confirmation.html", {"request": request, "ride": ride, "result": result})


@app.get("/bookings")
def get_local_bookings(request: Request):
    filepath = os.path.join("Data", "local_bookings.json")
    bookings = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                bookings = json.load(f)
        except Exception:
            pass
    return bookings


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

