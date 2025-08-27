# services/management/commands/seed_services.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.fields import Field
from decimal import Decimal
from services.models import Service

# ---- Deine Daten ----
BEAUTY_SERVICES = [
    # Hair Care (10)
    {"name": "Classic Haircut", "category": "Hair Care", "price": 25.00, "description": "Professional haircut for women and men"},
    {"name": "Hair Coloring", "category": "Hair Care", "price": 45.00, "description": "Hair coloring with premium products"},
    {"name": "Highlights", "category": "Hair Care", "price": 65.00, "description": "Modern highlighting technique for natural look"},
    {"name": "Perm", "category": "Hair Care", "price": 75.00, "description": "Long-lasting curls for more volume"},
    {"name": "Hair Conditioner Treatment", "category": "Hair Care", "price": 15.00, "description": "Intensive care treatment for damaged hair"},
    {"name": "Hair Straightening", "category": "Hair Care", "price": 85.00, "description": "Keratin straightening for shiny hair"},
    {"name": "Children's Haircut", "category": "Hair Care", "price": 18.00, "description": "Special haircut for children"},
    {"name": "Beard Trimming", "category": "Hair Care", "price": 12.00, "description": "Professional beard care and styling"},
    {"name": "Scalp Massage", "category": "Hair Care", "price": 20.00, "description": "Relaxing scalp massage with oils"},
    {"name": "Updo Hairstyle", "category": "Hair Care", "price": 35.00, "description": "Elegant hairstyle for special occasions"},

    # Cosmetics (8)
    {"name": "Professional Makeup", "category": "Cosmetics", "price": 45.00, "description": "Complete makeup for events and celebrations"},
    {"name": "Eyebrow Shaping", "category": "Cosmetics", "price": 15.00, "description": "Plucking and shaping of eyebrows"},
    {"name": "Eyelash Tinting", "category": "Cosmetics", "price": 18.00, "description": "Long-lasting eyelash coloring"},
    {"name": "Permanent Makeup", "category": "Cosmetics", "price": 250.00, "description": "Semi-permanent makeup for lips and eyes"},
    {"name": "Facial Cleansing", "category": "Cosmetics", "price": 55.00, "description": "Deep cleansing of facial skin"},
    {"name": "Permanent Makeup Correction", "category": "Cosmetics", "price": 120.00, "description": "Correction and refresh of permanent makeup"},
    {"name": "Brow Lamination", "category": "Cosmetics", "price": 35.00, "description": "Styling and smoothing of eyebrows"},
    {"name": "Facial Peeling", "category": "Cosmetics", "price": 40.00, "description": "Gentle peeling for radiant skin"},

    # Massage (8)
    {"name": "Classic Back Massage", "category": "Massage", "price": 50.00, "description": "30-minute relaxation massage for the back"},
    {"name": "Full Body Massage", "category": "Massage", "price": 80.00, "description": "60-minute massage of the entire body"},
    {"name": "Hot Stone Massage", "category": "Massage", "price": 75.00, "description": "Massage with warm stones for deep relaxation"},
    {"name": "Aromatherapy Massage", "category": "Massage", "price": 65.00, "description": "Massage with essential oils for wellness effect"},
    {"name": "Sports Massage", "category": "Massage", "price": 55.00, "description": "Intensive massage for athletes' recovery"},
    {"name": "Thai Massage", "category": "Massage", "price": 70.00, "description": "Traditional Thai massage technique"},
    {"name": "Head and Neck Massage", "category": "Massage", "price": 25.00, "description": "Relaxing massage of head and neck"},
    {"name": "Foot Reflexology", "category": "Massage", "price": 40.00, "description": "Massage of reflex zones on the feet"},

    # Nail Care (8)
    {"name": "Manicure", "category": "Nail Care", "price": 25.00, "description": "Complete hand and nail care"},
    {"name": "Pedicure", "category": "Nail Care", "price": 35.00, "description": "Comprehensive foot and nail care"},
    {"name": "Gel Nails", "category": "Nail Care", "price": 45.00, "description": "Extension and strengthening with gel nails"},
    {"name": "French Manicure", "category": "Nail Care", "price": 30.00, "description": "Classic French look for nails"},
    {"name": "Nail Repair", "category": "Nail Care", "price": 15.00, "description": "Repair of broken or damaged nails"},
    {"name": "Nail Art Design", "category": "Nail Care", "price": 20.00, "description": "Creative design with patterns and decorations"},
    {"name": "Paraffin Hand Treatment", "category": "Nail Care", "price": 25.00, "description": "Nourishing paraffin bath for tender hands"},
    {"name": "Nail Polish Application", "category": "Nail Care", "price": 12.00, "description": "Professional nail polish application"},

    # Wellness (8)
    {"name": "Sauna Infusion", "category": "Wellness", "price": 20.00, "description": "Refreshing sauna infusion with essential oils"},
    {"name": "Steam Bath", "category": "Wellness", "price": 15.00, "description": "Relaxing steam bath for respiratory system"},
    {"name": "Whirlpool", "category": "Wellness", "price": 25.00, "description": "Rejuvenating bath in whirlpool"},
    {"name": "Herbal Bath", "category": "Wellness", "price": 35.00, "description": "Soothing bath with natural herbs"},
    {"name": "Relaxation Bath", "category": "Wellness", "price": 30.00, "description": "Luxurious bath with bath additives"},
    {"name": "Infrared Cabin", "category": "Wellness", "price": 22.00, "description": "Gentle heat therapy in infrared cabin"},
    {"name": "Cryotherapy Chamber", "category": "Wellness", "price": 40.00, "description": "Invigorating cold therapy for circulation"},
    {"name": "Solarium", "category": "Wellness", "price": 10.00, "description": "Tanning in modern sunbed"},

    # Facial Treatment (8)
    {"name": "Anti-Aging Treatment", "category": "Facial Treatment", "price": 90.00, "description": "Intensive care against wrinkles and skin aging"},
    {"name": "Acne Treatment", "category": "Facial Treatment", "price": 70.00, "description": "Professional treatment for acne problems"},
    {"name": "Lifting Treatment", "category": "Facial Treatment", "price": 85.00, "description": "Firming treatment for facial skin"},
    {"name": "Oxygen Therapy", "category": "Facial Treatment", "price": 65.00, "description": "Revitalizing treatment with pure oxygen"},
    {"name": "Hyaluronic Acid Treatment", "category": "Facial Treatment", "price": 120.00, "description": "Moisturizing hyaluronic acid treatment"},
    {"name": "LED Light Therapy", "category": "Facial Treatment", "price": 55.00, "description": "Skin-regenerating light therapy"},
    {"name": "Microdermabrasion", "category": "Facial Treatment", "price": 75.00, "description": "Gentle peeling procedure for the skin"},
    {"name": "Facial Mask", "category": "Facial Treatment", "price": 35.00, "description": "Nourishing and caring facial mask"},
]

def field_names(model):
    return {f.name for f in model._meta.get_fields() if isinstance(f, Field)}

def pick_first_existing(fields_set, candidates):
    """Gibt den ersten Feldnamen zurück, der im Model existiert – sonst None."""
    for name in candidates:
        if name in fields_set:
            return name
    return None

class Command(BaseCommand):
    help = "Seed the database with beauty services. Idempotent. Auto-detects available fields."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete all existing services before seeding.")
        parser.add_argument("--dry-run", action="store_true", help="Show actions without writing to DB.")

    @transaction.atomic
    def handle(self, *args, **options):
        dry = options["dry_run"]
        reset = options["reset"]

        self.stdout.write("=== Seeding Beauty Services ===")

        # Model-Felder ermitteln
        model_fields = field_names(Service)
        # Mögliche Verfügbarkeits-Felder prüfen
        availability_field = pick_first_existing(
            model_fields, ["availability", "is_available", "active", "is_active", "enabled"]
        )
        # Optionale Felder prüfen
        category_field = pick_first_existing(model_fields, ["category", "service_category", "type"])
        description_field = pick_first_existing(model_fields, ["description", "details", "note", "notes"])
        price_field = pick_first_existing(model_fields, ["price", "amount", "cost"])

        if reset:
            cnt = Service.objects.count()
            if dry:
                self.stdout.write(f"[DRY-RUN] Would delete {cnt} services.")
            else:
                Service.objects.all().delete()
                self.stdout.write(f"🗑️  Deleted {cnt} services.")

        created = updated = 0

        for s in BEAUTY_SERVICES:
            # Lookup-Key: bevorzugt 'name', fallback auf (name+category), je nachdem was existiert
            if "name" not in model_fields:
                self.stderr.write("❌ Dein Service-Model hat kein 'name'-Feld. Bitte gib mir die Feldnamen.")
                return

            lookup = {"name": s["name"]}

            defaults = {}
            if description_field:
                defaults[description_field] = s["description"]
            if category_field:
                defaults[category_field] = s["category"]
            if price_field:
                defaults[price_field] = Decimal(str(s["price"]))
            if availability_field:
                defaults[availability_field] = True

            if dry:
                exists = Service.objects.filter(**lookup).exists()
                self.stdout.write(f"[DRY-RUN] Would {'update' if exists else 'create'}: {s['name']}")
                continue

            obj, was_created = Service.objects.update_or_create(defaults=defaults, **lookup)
            if was_created:
                self.stdout.write(f"✅ Created: {obj}")
                created += 1
            else:
                self.stdout.write(f"♻️  Updated: {obj}")
                updated += 1

        self.stdout.write("\n🎉 Done!")
        self.stdout.write(f"✅ Created: {created}")
        self.stdout.write(f"♻️  Updated: {updated}")
