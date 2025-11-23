"""
Create sample job postings for testing
Run this before testing the farmer side
"""
import sys
import os
# Add parent directory to path to import data_store
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_store import DataStore
from datetime import datetime

def create_sample_data():
    store = DataStore()

    # Create a sample farm owner
    owner_phone = "whatsapp:+15555550001"
    store.create_user(owner_phone, 'farm_owner')
    store.update_user(owner_phone, {'registered': True})
    store.update_user_profile(owner_phone, {
        'name': 'Sarah Johnson',
        'farm_name': 'Sunny Acres Farm',
        'location': 'Chapel Hill, NC'
    })

    # Create sample jobs with new detailed format
    jobs = [
        {
            "work_type": "Tobacco Harvesting",
            "pay_rate": 16.5,
            "location": "Chapel Hill, NC",
            "hours": "full-time",
            "workers_needed": 8,
            "description": "Harvest tobacco leaves. Must be comfortable working in humid conditions. Experience preferred but training provided. Transportation from central Chapel Hill.",
            "owner_phone": "whatsapp:+19195550001",
            "owner_name": "James Wilson",
            "farm_name": "Blue Ridge Farms"
        },
        {
            "work_type": "Sweet Potato Harvesting",
            "pay_rate": 17.0,
            "location": "Durham, NC",
            "hours": "full-time",
            "workers_needed": 6,
            "description": "Harvest sweet potatoes. Heavy lifting required. Paid weekly. Perfect for those with harvesting experience.",
            "owner_phone": "whatsapp:+19195550002",
            "owner_name": "Maria Rodriguez",
            "farm_name": "Carolina Sweet Farms"
        },
        {
            "work_type": "Strawberry Picking",
            "pay_rate": 15.5,
            "location": "Raleigh, NC",
            "hours": "part-time",
            "workers_needed": 10,
            "description": "Pick strawberries during morning hours. Family-friendly environment. Great for students or part-time workers. Piece rate also available.",
            "owner_phone": "whatsapp:+19195550002",
            "owner_name": "Maria Rodriguez",
            "farm_name": "Carolina Sweet Farms"
        },
        {
            "work_type": "Greenhouse Work",
            "pay_rate": 18.0,
            "location": "Carrboro, NC",
            "hours": "full-time",
            "workers_needed": 3,
            "description": "Maintain greenhouse plants, water, transplant seedlings. Climate-controlled environment. Good for year-round work.",
            "owner_phone": "whatsapp:+19195550003",
            "owner_name": "David Chen",
            "farm_name": "Green Leaf Gardens"
        },
        {
            "work_type": "Livestock Care",
            "pay_rate": 19.0,
            "location": "Hillsborough, NC",
            "hours": "flexible",
            "workers_needed": 2,
            "description": "Care for cattle and pigs. Feed animals, clean barns, assist with veterinary care. Early morning start required.",
            "owner_phone": "whatsapp:+19195550003",
            "owner_name": "David Chen",
            "farm_name": "Green Leaf Gardens"
        },
        {
            "work_type": "Organic Vegetable Farming",
            "pay_rate": 20.0,
            "location": "Chapel Hill, NC",
            "hours": "full-time",
            "workers_needed": 4,
            "description": "Work on certified organic farm. Plant, weed, harvest various vegetables. Knowledge of organic methods a plus. Health benefits available.",
            "owner_phone": "whatsapp:+19195550001",
            "owner_name": "James Wilson",
            "farm_name": "Blue Ridge Farms"
        },
        {
            "work_type": "Equipment Maintenance",
            "pay_rate": 22.0,
            "location": "Pittsboro, NC",
            "hours": "full-time",
            "workers_needed": 1,
            "description": "Maintain and repair farm equipment including tractors and harvesters. Mechanical experience required. Higher pay for certified mechanics.",
            "owner_phone": "whatsapp:+19195550004",
            "owner_name": "Robert Taylor",
            "farm_name": "Taylor Agricultural Services"
        },
        {
            "work_type": "Irrigation Specialist",
            "pay_rate": 21.0,
            "location": "Cary, NC",
            "hours": "full-time",
            "workers_needed": 2,
            "description": "Install and maintain drip irrigation systems. Experience with modern irrigation technology preferred. Company truck provided.",
            "owner_phone": "whatsapp:+19195550004",
            "owner_name": "Robert Taylor",
            "farm_name": "Taylor Agricultural Services"
        },
        {
            "work_type": "Blueberry Harvesting",
            "pay_rate": 16.0,
            "location": "Southern Pines, NC",
            "hours": "seasonal",
            "workers_needed": 15,
            "description": "Peak season blueberry harvest. June-August work. Piece rate available for experienced pickers. Housing assistance available for seasonal workers.",
            "owner_phone": "whatsapp:+19195550005",
            "owner_name": "Linda Brown",
            "farm_name": "Piedmont Berry Farm"
        },
        {
            "work_type": "General Farm Labor",
            "pay_rate": 17.5,
            "location": "Chapel Hill, NC",
            "hours": "full-time",
            "workers_needed": 5,
            "description": "Various farm tasks including planting, weeding, harvesting, and maintenance. Good entry-level position. Training provided.",
            "owner_phone": "whatsapp:+19195550001",
            "owner_name": "James Wilson",
            "farm_name": "Blue Ridge Farms"
        },
        # Additional Chapel Hill area jobs
        {
            "work_type": "Tomato Harvesting",
            "pay_rate": 19.0,
            "location": "Chapel Hill, NC",
            "hours": "full-time",
            "workers_needed": 8,
            "description": "Peak tomato season. Hand-pick ripe tomatoes. Experience preferred but will train. Early morning start.",
            "owner_phone": "whatsapp:+19195550001",
            "owner_name": "James Wilson",
            "farm_name": "Blue Ridge Farms"
        },
        {
            "work_type": "Cucumber Harvesting",
            "pay_rate": 16.5,
            "location": "Chapel Hill, NC",
            "hours": "part-time",
            "workers_needed": 4,
            "description": "Morning shifts only (6 AM - 12 PM). Perfect for students or part-time workers. Piece rate available.",
            "owner_phone": "whatsapp:+19195550006",
            "owner_name": "Maria Garcia",
            "farm_name": "Chapel Hill Community Farm"
        },
        {
            "work_type": "Lettuce Planting",
            "pay_rate": 15.5,
            "location": "Chapel Hill, NC",
            "hours": "flexible",
            "workers_needed": 3,
            "description": "Plant lettuce seedlings. Flexible schedule. Good for beginners. Gloves and tools provided.",
            "owner_phone": "whatsapp:+19195550006",
            "owner_name": "Maria Garcia",
            "farm_name": "Chapel Hill Community Farm"
        },
        {
            "work_type": "Pepper Harvesting",
            "pay_rate": 18.0,
            "location": "Carrboro, NC",
            "hours": "full-time",
            "workers_needed": 6,
            "description": "Bell pepper and hot pepper harvest. Climate-controlled greenhouse work. Year-round position available.",
            "owner_phone": "whatsapp:+19195550003",
            "owner_name": "David Chen",
            "farm_name": "Green Leaf Gardens"
        },
        {
            "work_type": "Berry Picking",
            "pay_rate": 17.0,
            "location": "Carrboro, NC",
            "hours": "part-time",
            "workers_needed": 10,
            "description": "Strawberry and blackberry picking. Seasonal work April-July. Family-friendly environment. Piece rate bonus available.",
            "owner_phone": "whatsapp:+19195550007",
            "owner_name": "Susan Martinez",
            "farm_name": "Carrboro Berry Fields"
        },
        {
            "work_type": "Vegetable Weeding",
            "pay_rate": 14.5,
            "location": "Carrboro, NC",
            "hours": "flexible",
            "workers_needed": 5,
            "description": "Weed vegetable rows. Simple work, no experience needed. Morning or afternoon shifts available.",
            "owner_phone": "whatsapp:+19195550007",
            "owner_name": "Susan Martinez",
            "farm_name": "Carrboro Berry Fields"
        },
        {
            "work_type": "Squash Harvesting",
            "pay_rate": 16.0,
            "location": "Durham, NC",
            "hours": "full-time",
            "workers_needed": 4,
            "description": "Harvest zucchini, yellow squash, and butternut squash. Physical work. Reliable transportation helpful.",
            "owner_phone": "whatsapp:+19195550002",
            "owner_name": "Maria Rodriguez",
            "farm_name": "Carolina Sweet Farms"
        },
        {
            "work_type": "Corn Detasseling",
            "pay_rate": 15.0,
            "location": "Durham, NC",
            "hours": "part-time",
            "workers_needed": 12,
            "description": "Summer seasonal work. Remove tassels from corn plants. Good for teens and students. July-August only.",
            "owner_phone": "whatsapp:+19195550008",
            "owner_name": "Tom Jenkins",
            "farm_name": "Durham Valley Farms"
        },
        {
            "work_type": "Pumpkin Harvesting",
            "pay_rate": 17.5,
            "location": "Hillsborough, NC",
            "hours": "full-time",
            "workers_needed": 7,
            "description": "Fall harvest season. Load and transport pumpkins. Heavy lifting required. Weekends mandatory in October.",
            "owner_phone": "whatsapp:+19195550009",
            "owner_name": "Patricia Brown",
            "farm_name": "Hillsborough Pumpkin Patch"
        },
        {
            "work_type": "Apple Picking",
            "pay_rate": 16.5,
            "location": "Hillsborough, NC",
            "hours": "flexible",
            "workers_needed": 15,
            "description": "Pick apples using ladders and baskets. September-October peak season. Piece rate incentives. All experience levels welcome.",
            "owner_phone": "whatsapp:+19195550009",
            "owner_name": "Patricia Brown",
            "farm_name": "Hillsborough Pumpkin Patch"
        },
        {
            "work_type": "Farm Stand Attendant",
            "pay_rate": 14.0,
            "location": "Chapel Hill, NC",
            "hours": "part-time",
            "workers_needed": 2,
            "description": "Sell produce at farm stand. Customer service skills needed. Weekend availability required. Indoor work.",
            "owner_phone": "whatsapp:+19195550006",
            "owner_name": "Maria Garcia",
            "farm_name": "Chapel Hill Community Farm"
        },
        {
            "work_type": "Herb Harvesting",
            "pay_rate": 15.0,
            "location": "Chapel Hill, NC",
            "hours": "flexible",
            "workers_needed": 3,
            "description": "Harvest and bundle fresh herbs (basil, cilantro, parsley). Gentle work. Attention to detail important.",
            "owner_phone": "whatsapp:+19195550006",
            "owner_name": "Maria Garcia",
            "farm_name": "Chapel Hill Community Farm"
        },
        {
            "work_type": "Flower Planting",
            "pay_rate": 15.5,
            "location": "Carrboro, NC",
            "hours": "part-time",
            "workers_needed": 4,
            "description": "Plant seasonal flowers and ornamentals. Spring work March-May. Pleasant outdoor work. Perfect for detail-oriented workers.",
            "owner_phone": "whatsapp:+19195550007",
            "owner_name": "Susan Martinez",
            "farm_name": "Carrboro Berry Fields"
        },
        {
            "work_type": "Composting",
            "pay_rate": 14.5,
            "location": "Chapel Hill, NC",
            "hours": "full-time",
            "workers_needed": 2,
            "description": "Turn compost piles, manage organic waste. Physical work. Environmental experience a plus. Year-round position.",
            "owner_phone": "whatsapp:+19195550001",
            "owner_name": "James Wilson",
            "farm_name": "Blue Ridge Farms"
        },
        {
            "work_type": "Kale Harvesting",
            "pay_rate": 16.0,
            "location": "Durham, NC",
            "hours": "part-time",
            "workers_needed": 5,
            "description": "Morning harvest of kale and other greens. Cool weather work Oct-April. Early birds welcome. 5 AM - 11 AM shifts.",
            "owner_phone": "whatsapp:+19195550002",
            "owner_name": "Maria Rodriguez",
            "farm_name": "Carolina Sweet Farms"
        }
    ]

    print("Creating sample jobs...\n")

    for job in jobs:
        job_id = store.create_job(job)
        # Handle both old and new payment formats
        if 'payment_amount' in job:
            pay_str = f"${job['payment_amount']} {job['payment_type']}"
        else:
            pay_str = f"${job['pay_rate']}/hr"
        print(f"✅ Created: {job['work_type']} - {pay_str} - {job['location']}")
        print(f"   Job ID: {job_id}\n")

    print(f"\n🎉 Sample data created successfully!")
    print(f"📊 Total jobs: {len(jobs)}")
    print(f"👨‍🌾 Farm owner: {owner_phone}")
    print(f"\nYou can now test the farmer side of the chatbot!")

if __name__ == "__main__":
    create_sample_data()
