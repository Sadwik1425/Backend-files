import os
import django
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mri_backend.settings')
django.setup()

from protocols.models import Region, Indication

def seed():
    data = {
        "Brain": [
            "Acute ischemic stroke",
            "Multiple sclerosis (Routine survey)",
            "Brain tumor (Pre-op survey)",
            "Seizure protocol",
            "Headache / Screening",
            "Intracranial hemorrhage"
        ],
        "Spine": [
            "Radiculopathy / Disc herniation",
            "Spinal cord injury / Myelopathy",
            "Metastatic survey",
            "Infection / Discitis",
            "Post-operative spine",
            "Spine Trauma / Fracture"
        ],
        "Upper Limb": [
            "Rotator cuff / Shoulder injury",
            "Nerve / Fluid assessment",
            "Bone marrow survey",
            "Joint pathology"
        ],
        "Lower Limb": [
            "ACL/MCL/Meniscal injury (Knee)",
            "Avascular necrosis (Hip)",
            "Osteochondral defect",
            "Joint instability"
        ],
        "Chest": [
            "Brachial plexus / Thoracic outlet",
            "Mediastinal mass survey",
            "Chest wall pathology"
        ],
        "Cardiac": [
            "Ventricular function / Volumes",
            "Myocarditis / Viability / Infarct",
            "Cardiac output assessment"
        ],
        "Abdomen": [
            "Liver lesion characterization / HCC",
            "MRCP (Biliary survey)",
            "Renal mass evaluation",
            "Pancreatic protocol / Pancreatitis",
            "Adrenal mass"
        ],
        "Pelvis": [
            "Prostate / Cancer staging",
            "Endometriosis / Adenomyosis / Fibroid",
            "Pelvic oncology staging",
            "Gynae / Uterine survey"
        ],
        "Vascular": [
            "Arterial MRA / Aneurysm / Stenosis",
            "Venous MRV / Thrombosis",
            "Non-contrast vascular flow"
        ],
        "Whole Body": [
            "Multiple myeloma screening",
            "Metastatic screening survey"
        ]
    }

    for region_name, indications in data.items():
        region, _ = Region.objects.get_or_create(name=region_name)
        for ind_name in indications:
            Indication.objects.get_or_create(region=region, name=ind_name)
        print(f"Seeded {region_name}")

if __name__ == "__main__":
    seed()
