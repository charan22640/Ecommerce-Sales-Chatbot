"""
Enhanced Electronics Store Seed Data
Comprehensive product database with realistic specifications and features
"""
import json
from app.models.product import Product

def get_electronics_products():
    """Return a comprehensive list of electronics products with detailed specifications."""
    
    products = [
        # SMARTPHONES
        {
            "name": "iPhone 15 Pro Max",
            "description": "Latest flagship iPhone with titanium design, A17 Pro chip, and pro camera system",
            "price": 1199.99,
            "category": "smartphones",
            "subcategory": "flagship",
            "style": "premium",
            "color": "space-gray",
            "size": "512GB",
            "rating": 4.8,
            "stock_quantity": 15,
            "brand": "Apple",
            "model": "iPhone 15 Pro Max",
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
            "specifications": json.dumps({
                "display": "6.7-inch Super Retina XDR",
                "processor": "A17 Pro chip",
                "camera": "48MP main + 12MP ultra-wide + 12MP telephoto",
                "battery": "Up to 29 hours video playback",
                "storage": "512GB",
                "operating_system": "iOS 17",
                "connectivity": "5G, Wi-Fi 6E, Bluetooth 5.3",
                "build": "Titanium frame with Ceramic Shield front"
            }),
            "features": json.dumps([
                "premium build quality",
                "high performance",
                "professional photography",
                "long battery life",
                "5G connectivity"
            ])
        },
        
        {
            "name": "Samsung Galaxy S24 Ultra",
            "description": "Android flagship with S Pen, 200MP camera, and AI features",
            "price": 1299.99,
            "category": "smartphones",
            "subcategory": "flagship",
            "style": "premium",
            "color": "black",
            "size": "1TB",
            "rating": 4.7,
            "stock_quantity": 12,
            "brand": "Samsung",
            "model": "Galaxy S24 Ultra",
            "image_url": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=800",
            "specifications": json.dumps({
                "display": "6.8-inch Dynamic AMOLED 2X, 120Hz",
                "processor": "Snapdragon 8 Gen 3",
                "camera": "200MP main + 50MP periscope + 12MP ultra-wide + 10MP telephoto",
                "battery": "5000mAh with 45W fast charging",
                "storage": "1TB",
                "operating_system": "Android 14 with One UI 6.1",
                "connectivity": "5G, Wi-Fi 7, Bluetooth 5.3",
                "special_features": "S Pen included, AI photo editing"
            }),
            "features": json.dumps([
                "premium build quality",
                "high performance",
                "professional photography",
                "s pen included",
                "ai features"
            ])
        },
        
        {
            "name": "Google Pixel 8 Pro",
            "description": "AI-powered Android phone with exceptional camera and pure Google experience",
            "price": 899.99,
            "category": "smartphones",
            "subcategory": "flagship",
            "style": "premium",
            "color": "white",
            "size": "256GB",
            "rating": 4.6,
            "stock_quantity": 20,
            "brand": "Google",
            "model": "Pixel 8 Pro",
            "image_url": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=800",
            "specifications": json.dumps({
                "display": "6.7-inch LTPO OLED, 120Hz",
                "processor": "Google Tensor G3",
                "camera": "50MP main + 48MP ultra-wide + 48MP telephoto",
                "battery": "5050mAh with 30W fast charging",
                "storage": "256GB",
                "operating_system": "Android 14",
                "connectivity": "5G, Wi-Fi 7, Bluetooth 5.3",
                "ai_features": "Magic Eraser, Live Translate, Call Screen"
            }),
            "features": json.dumps([
                "ai photography",
                "pure android experience",
                "long software support",
                "wireless charging",
                "water resistant"
            ])
        },
        
        {
            "name": "OnePlus 12R",
            "description": "High-performance gaming phone with flagship features at mid-range price",
            "price": 599.99,
            "category": "smartphones",
            "subcategory": "gaming",
            "style": "gaming",
            "color": "blue",
            "size": "256GB",
            "rating": 4.5,
            "stock_quantity": 25,
            "brand": "OnePlus",
            "model": "12R",
            "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=800",
            "specifications": json.dumps({
                "display": "6.78-inch AMOLED, 120Hz",
                "processor": "Snapdragon 8 Gen 2",
                "camera": "50MP main + 8MP ultra-wide + 2MP macro",
                "battery": "5500mAh with 100W SuperVOOC charging",
                "storage": "256GB",
                "operating_system": "OxygenOS 14 (Android 14)",
                "connectivity": "5G, Wi-Fi 7, Bluetooth 5.3",
                "gaming_features": "Game Space, HyperBoost Gaming Engine"
            }),
            "features": json.dumps([
                "high performance gaming",
                "ultra fast charging",
                "smooth display",
                "value for money",
                "gaming optimized"
            ])
        },
        
        # LAPTOPS
        {
            "name": "MacBook Pro 16-inch M3 Max",
            "description": "Professional laptop with M3 Max chip, perfect for creative work and development",
            "price": 2999.99,
            "category": "computers",
            "subcategory": "laptops",
            "style": "professional",
            "color": "space-gray",
            "size": "1TB",
            "rating": 4.9,
            "stock_quantity": 8,
            "brand": "Apple",
            "model": "MacBook Pro 16-inch",
            "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800",
            "specifications": json.dumps({
                "display": "16.2-inch Liquid Retina XDR (3456×2234)",
                "processor": "Apple M3 Max chip with 16-core CPU",
                "graphics": "40-core GPU",
                "memory": "36GB unified memory",
                "storage": "1TB SSD",
                "battery": "Up to 22 hours video playback",
                "ports": "3x Thunderbolt 4, HDMI, SD card, MagSafe 3",
                "operating_system": "macOS Sonoma"
            }),
            "features": json.dumps([
                "professional performance",
                "long battery life",
                "premium build quality",
                "creative work optimized",
                "silent operation"
            ])
        },
        
        {
            "name": "ASUS ROG Strix G17",
            "description": "High-performance gaming laptop with RTX 4070 and advanced cooling",
            "price": 1899.99,
            "category": "computers",
            "subcategory": "laptops",
            "style": "gaming",
            "color": "black",
            "size": "1TB",
            "rating": 4.6,
            "stock_quantity": 12,
            "brand": "ASUS",
            "model": "ROG Strix G17",
            "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800",
            "specifications": json.dumps({
                "display": "17.3-inch FHD 144Hz IPS",
                "processor": "AMD Ryzen 9 7940HX",
                "graphics": "NVIDIA GeForce RTX 4070 8GB",
                "memory": "32GB DDR5",
                "storage": "1TB PCIe SSD",
                "keyboard": "RGB backlit with anti-ghosting",
                "cooling": "Intelligent Cooling with liquid metal",
                "operating_system": "Windows 11 Pro"
            }),
            "features": json.dumps([
                "high performance gaming",
                "advanced cooling system",
                "rgb lighting",
                "high refresh rate display",
                "vr ready"
            ])
        },
        
        {
            "name": "Dell XPS 13 Plus",
            "description": "Ultra-premium ultrabook with stunning design and performance",
            "price": 1299.99,
            "category": "computers",
            "subcategory": "laptops",
            "style": "premium",
            "color": "silver",
            "size": "512GB",
            "rating": 4.7,
            "stock_quantity": 15,
            "brand": "Dell",
            "model": "XPS 13 Plus",
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800",
            "specifications": json.dumps({
                "display": "13.4-inch 3.5K OLED Touch Display",
                "processor": "Intel Core i7-1360P",
                "graphics": "Intel Iris Xe Graphics",
                "memory": "16GB LPDDR5",
                "storage": "512GB PCIe NVMe SSD",
                "battery": "Up to 12 hours",
                "build": "CNC machined aluminum",
                "operating_system": "Windows 11 Home"
            }),
            "features": json.dumps([
                "premium build quality",
                "oled display",
                "ultraportable design",
                "long battery life",
                "business professional"
            ])
        },
        
        {
            "name": "Lenovo ThinkPad X1 Carbon",
            "description": "Business ultrabook with military-grade durability and security features",
            "price": 1599.99,
            "category": "computers",
            "subcategory": "laptops",
            "style": "professional",
            "color": "black",
            "size": "512GB",
            "rating": 4.8,
            "stock_quantity": 18,
            "brand": "Lenovo",
            "model": "ThinkPad X1 Carbon",
            "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=800",
            "specifications": json.dumps({
                "display": "14-inch 2.8K OLED Display",
                "processor": "Intel Core i7-1355U",
                "graphics": "Intel Iris Xe Graphics",
                "memory": "16GB LPDDR5",
                "storage": "512GB PCIe SSD",
                "security": "Fingerprint reader, TPM 2.0, IR camera",
                "durability": "MIL-STD-810H tested",
                "operating_system": "Windows 11 Pro"
            }),
            "features": json.dumps([
                "business professional",
                "military grade durability",
                "advanced security",
                "lightweight design",
                "long battery life"
            ])
        },
        
        # AUDIO PRODUCTS
        {
            "name": "Sony WH-1000XM5",
            "description": "Industry-leading noise canceling headphones with exceptional sound quality",
            "price": 399.99,
            "category": "audio",
            "subcategory": "headphones",
            "style": "premium",
            "color": "black",
            "size": "Over-ear",
            "rating": 4.8,
            "stock_quantity": 30,
            "brand": "Sony",
            "model": "WH-1000XM5",
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800",
            "specifications": json.dumps({
                "driver_size": "30mm",
                "frequency_response": "4Hz-40kHz",
                "battery_life": "30 hours with ANC",
                "charging": "USB-C, 3 min charge = 3 hours playback",
                "connectivity": "Bluetooth 5.2, LDAC, multipoint",
                "noise_cancellation": "Dual Noise Sensor technology",
                "microphones": "8 microphones for calls and ANC"
            }),
            "features": json.dumps([
                "industry leading noise cancellation",
                "high bass response",
                "premium sound quality",
                "long battery life",
                "quick charge",
                "multipoint connection"
            ])
        },
        
        {
            "name": "JBL Charge 5",
            "description": "Portable Bluetooth speaker with powerful sound and power bank function",
            "price": 149.99,
            "category": "audio",
            "subcategory": "speakers",
            "style": "portable",
            "color": "blue",
            "size": "Portable",
            "rating": 4.6,
            "stock_quantity": 40,
            "brand": "JBL",
            "model": "Charge 5",
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",
            "specifications": json.dumps({
                "driver_configuration": "1x racetrack driver + 2x JBL bass radiators",
                "power_output": "40W RMS",
                "frequency_response": "65Hz - 20kHz",
                "battery_life": "20 hours playtime",
                "charging": "USB-C, can charge other devices",
                "waterproof": "IP67 waterproof and dustproof",
                "connectivity": "Bluetooth 5.1, JBL PartyBoost"
            }),
            "features": json.dumps([
                "high volume output",
                "deep bass response",
                "waterproof design",
                "power bank function",
                "party boost compatible",
                "long battery life"
            ])
        },
        
        {
            "name": "Bose QuietComfort Earbuds",
            "description": "True wireless earbuds with world-class noise cancellation",
            "price": 279.99,
            "category": "audio",
            "subcategory": "earbuds",
            "style": "premium",
            "color": "white",
            "size": "True Wireless",
            "rating": 4.7,
            "stock_quantity": 25,
            "brand": "Bose",
            "model": "QuietComfort Earbuds",
            "image_url": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800",
            "specifications": json.dumps({
                "driver_size": "6mm",
                "battery_life": "6 hours + 12 hours with case",
                "charging": "USB-C, wireless charging compatible",
                "noise_cancellation": "11 levels of active noise cancellation",
                "connectivity": "Bluetooth 5.1",
                "controls": "Touch controls with customizable settings",
                "water_resistance": "IPX4 sweat and weather resistant"
            }),
            "features": json.dumps([
                "world class noise cancellation",
                "premium sound quality",
                "comfortable fit",
                "wireless charging",
                "sweat resistant",
                "long battery life"
            ])
        },
        
        {
            "name": "Klipsch R-51PM",
            "description": "Powered bookshelf speakers with dynamic sound for music and gaming",
            "price": 379.99,
            "category": "audio",
            "subcategory": "speakers",
            "style": "professional",
            "color": "black",
            "size": "Bookshelf",
            "rating": 4.7,
            "stock_quantity": 15,
            "brand": "Klipsch",
            "model": "R-51PM",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
            "specifications": json.dumps({
                "driver_configuration": "5.25-inch copper-spun woofer + 1-inch aluminum LTS tweeter",
                "power_output": "340W peak system power",
                "frequency_response": "62Hz - 25kHz",
                "inputs": "Bluetooth, USB, analog, optical digital",
                "amplification": "Built-in amplifiers",
                "controls": "Front panel controls with remote",
                "dimensions": "13.9 x 7.0 x 9.25 inches per speaker"
            }),
            "features": json.dumps([
                "high volume capability",
                "deep bass response",
                "professional sound quality",
                "multiple input options",
                "gaming optimized",
                "room filling sound"
            ])
        },
          # GAMING PRODUCTS
        {
            "name": "PlayStation 5",
            "description": "Next-gen gaming console with 4K gaming and ultra-fast SSD",
            "price": 499.99,
            "category": "gaming",
            "subcategory": "consoles",
            "style": "gaming",
            "color": "white",
            "size": "825GB",
            "rating": 4.8,
            "stock_quantity": 20,
            "brand": "Sony",
            "model": "PlayStation 5",
            "image_url": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=800",
            "specifications": json.dumps({
                "processor": "Custom AMD Zen 2 8-core CPU",
                "graphics": "Custom AMD RDNA 2 GPU (10.28 TFLOPs)",
                "memory": "16GB GDDR6",
                "storage": "825GB custom NVMe SSD",
                "optical_drive": "4K UHD Blu-ray drive",
                "audio": "Tempest 3D AudioTech",
                "ray_tracing": "Hardware-accelerated ray tracing",
                "backwards_compatibility": "PS4 game compatibility"
            }),
            "features": json.dumps([
                "4k gaming support",
                "ultra fast loading",
                "ray tracing support",
                "3d audio",
                "haptic feedback controller",
                "high performance gaming"
            ])
        },
        
        {
            "name": "Xbox Series X",
            "description": "Most powerful Xbox console with 4K gaming and Quick Resume",
            "price": 499.99,
            "category": "gaming",
            "subcategory": "consoles",
            "style": "gaming",
            "color": "black",
            "size": "1TB",
            "rating": 4.7,
            "stock_quantity": 18,
            "brand": "Microsoft",
            "model": "Xbox Series X",
            "image_url": "https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=800",
            "specifications": json.dumps({
                "processor": "Custom AMD Zen 2 8-core CPU (3.8GHz)",
                "graphics": "Custom AMD RDNA 2 GPU (12 TFLOPs)",
                "memory": "16GB GDDR6",
                "storage": "1TB custom NVMe SSD",
                "optical_drive": "4K UHD Blu-ray drive",
                "quick_resume": "Resume multiple games instantly",
                "backwards_compatibility": "4 generations of Xbox games",
                "auto_hdr": "Automatic HDR enhancement"
            }),
            "features": json.dumps([
                "most powerful xbox",
                "4k gaming support",
                "quick resume feature",
                "backwards compatibility",
                "auto hdr",
                "high performance gaming"
            ])
        },
        
        {
            "name": "SteelSeries Arctis 7P",
            "description": "Wireless gaming headset with lossless audio and comfort design",
            "price": 169.99,
            "category": "gaming",
            "subcategory": "headsets",
            "style": "gaming",
            "color": "black",
            "size": "Over-ear",
            "rating": 4.6,
            "stock_quantity": 35,
            "brand": "SteelSeries",
            "model": "Arctis 7P",
            "image_url": "https://images.unsplash.com/photo-1599669454699-248893623440?w=800",
            "specifications": json.dumps({
                "driver_size": "40mm neodymium drivers",
                "frequency_response": "20Hz - 20kHz",
                "battery_life": "24+ hours",
                "connectivity": "2.4GHz wireless, USB-C",
                "microphone": "ClearCast bidirectional microphone",
                "compatibility": "PS5, PS4, PC, Switch, mobile",
                "audio": "DTS Headphone:X v2.0 surround sound"
            }),
            "features": json.dumps([
                "wireless gaming audio",
                "long battery life",
                "crystal clear microphone",
                "gaming optimized",
                "comfortable design",
                "multi platform support"
            ])
        },
        
        {
            "name": "Razer DeathAdder V3 Pro",
            "description": "Professional gaming mouse with Focus Pro sensor and wireless connectivity",
            "price": 149.99,
            "category": "gaming",
            "subcategory": "mice",
            "style": "gaming",
            "color": "black",
            "size": "Ergonomic",
            "rating": 4.8,
            "stock_quantity": 40,
            "brand": "Razer",
            "model": "DeathAdder V3 Pro",
            "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800",
            "specifications": json.dumps({
                "sensor": "Focus Pro 30K optical sensor",
                "dpi": "Up to 30,000 DPI",
                "polling_rate": "8000Hz HyperPolling",
                "battery_life": "90 hours",
                "connectivity": "HyperSpeed Wireless + Bluetooth",
                "switches": "90M click Razer optical switches",
                "weight": "63g ultralight design",
                "rgb": "Razer Chroma RGB lighting"
            }),
            "features": json.dumps([
                "professional gaming precision",
                "ultra lightweight design",
                "wireless connectivity",
                "long battery life",
                "high dpi sensor",
                "gaming optimized"
            ])
        }
    ]
    
    return products

def get_budget_electronics():
    """Return budget-friendly electronics with good value propositions."""
    
    budget_products = [
        {
            "name": "Xiaomi Redmi Note 13 Pro",
            "description": "Budget smartphone with flagship features, great camera, and fast charging",
            "price": 299.99,
            "category": "smartphones",
            "subcategory": "budget",
            "style": "budget",
            "color": "blue",
            "size": "256GB",
            "rating": 4.4,
            "stock_quantity": 50,
            "brand": "Xiaomi",
            "model": "Redmi Note 13 Pro",
            "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
            "specifications": json.dumps({
                "display": "6.67-inch AMOLED, 120Hz",
                "processor": "MediaTek Dimensity 7200-Ultra",
                "camera": "200MP main + 8MP ultra-wide + 2MP macro",
                "battery": "5100mAh with 67W fast charging",
                "storage": "256GB",
                "operating_system": "MIUI 14 (Android 13)",
                "connectivity": "5G, Wi-Fi 6, Bluetooth 5.3"
            }),
            "features": json.dumps([
                "budget friendly",
                "value for money",
                "fast charging",
                "good camera quality",
                "5g connectivity"
            ])
        },
        
        {
            "name": "Anker Soundcore Life Q30",
            "description": "Budget noise-canceling headphones with impressive sound quality",
            "price": 79.99,
            "category": "audio",
            "subcategory": "headphones",
            "style": "budget",
            "color": "black",
            "size": "Over-ear",
            "rating": 4.5,
            "stock_quantity": 60,
            "brand": "Anker",
            "model": "Soundcore Life Q30",
            "image_url": "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800",
            "specifications": json.dumps({
                "driver_size": "40mm dynamic drivers",
                "frequency_response": "16Hz - 40kHz",
                "battery_life": "40 hours with ANC off, 60 hours with ANC on",
                "charging": "USB-C, 5 min charge = 4 hours playback",
                "noise_cancellation": "Hybrid active noise canceling",
                "connectivity": "Bluetooth 5.0, 3.5mm aux",
                "app_support": "Soundcore app with EQ"
            }),
            "features": json.dumps([
                "budget friendly",
                "noise cancellation",
                "long battery life",
                "good bass response",
                "value for money",
                "app customization"
            ])
        },
        
        {
            "name": "Acer Aspire 5",
            "description": "Budget laptop perfect for students and everyday computing",
            "price": 449.99,
            "category": "computers",
            "subcategory": "laptops",
            "style": "student",
            "color": "silver",
            "size": "512GB",
            "rating": 4.2,
            "stock_quantity": 30,
            "brand": "Acer",
            "model": "Aspire 5",
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800",
            "specifications": json.dumps({
                "display": "15.6-inch Full HD IPS",
                "processor": "AMD Ryzen 5 7520U",
                "graphics": "AMD Radeon Graphics",
                "memory": "8GB DDR4",
                "storage": "512GB PCIe SSD",
                "battery": "Up to 7.5 hours",
                "ports": "USB 3.2, USB-C, HDMI, ethernet",
                "operating_system": "Windows 11 Home"
            }),
            "features": json.dumps([
                "budget friendly",
                "student laptop",
                "everyday computing",
                "good performance",
                "value for money",
                "portable design"
            ])        },
        
        # Smart TVs
        {
            "name": "Samsung 65-inch 4K QLED Smart TV",
            "description": "Premium 65-inch QLED smart TV with quantum dot technology and vibrant colors. Features smart platform with streaming apps.",
            "price": 1299.99,
            "category": "TV & Display",
            "brand": "Samsung",
            "model": "QN65Q70D",
            "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800",
            "specifications": json.dumps({
                "display_size": "65 inches",
                "resolution": "4K Ultra HD (3840x2160)",
                "display_type": "QLED",
                "refresh_rate": "120Hz",
                "smart_platform": "Tizen OS",
                "connectivity": "Wi-Fi 6, Bluetooth 5.2",
                "ports": "4x HDMI 2.1, 2x USB, Ethernet",
                "audio": "Dolby Atmos, 20W speakers"
            }),
            "features": json.dumps([
                "quantum dot technology",
                "4K upscaling",
                "gaming mode",
                "voice control",
                "streaming apps",
                "HDR10+ support"
            ])
        },
        
        {
            "name": "LG 55-inch OLED Smart TV",
            "description": "Stunning 55-inch OLED TV with perfect blacks and infinite contrast. Premium viewing experience with webOS platform.",
            "price": 1499.99,
            "category": "TV & Display",
            "brand": "LG",
            "model": "OLED55C3PUA",
            "image_url": "https://images.unsplash.com/photo-1567690187548-f07b1d7bf5a9?w=800",
            "specifications": json.dumps({
                "display_size": "55 inches",
                "resolution": "4K Ultra HD (3840x2160)",
                "display_type": "OLED",
                "refresh_rate": "120Hz",
                "smart_platform": "webOS 23",
                "connectivity": "Wi-Fi 6, Bluetooth 5.1",
                "ports": "4x HDMI 2.1, 3x USB, Ethernet",
                "audio": "Dolby Vision IQ, 40W speakers"
            }),
            "features": json.dumps([
                "perfect blacks",
                "infinite contrast",
                "gaming optimizer",
                "AI picture processing",
                "magic remote",
                "filmmaker mode"
            ])
        },
        
        # Tablets
        {
            "name": "iPad Pro 12.9-inch M2",
            "description": "Professional-grade tablet with M2 chip and Liquid Retina XDR display. Perfect for creative work and productivity.",
            "price": 1099.99,
            "category": "Tablet",
            "brand": "Apple",
            "model": "iPad Pro 12.9 M2",
            "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800",
            "specifications": json.dumps({
                "display": "12.9-inch Liquid Retina XDR",
                "processor": "Apple M2 chip",
                "storage": "128GB",
                "camera": "12MP Wide, 10MP Ultra Wide",
                "battery": "Up to 10 hours",
                "connectivity": "Wi-Fi 6E, 5G (Cellular models)",
                "accessories": "Apple Pencil 2nd gen compatible",
                "operating_system": "iPadOS 17"
            }),
            "features": json.dumps([
                "professional performance",
                "apple pencil support",
                "liquid retina display",
                "all-day battery",
                "USB-C connectivity",
                "face ID security"
            ])
        },
        
        {
            "name": "Samsung Galaxy Tab S9",
            "description": "Premium Android tablet with S Pen included. Perfect for productivity, creativity, and entertainment.",
            "price": 799.99,
            "category": "Tablet",
            "brand": "Samsung",
            "model": "Galaxy Tab S9",
            "image_url": "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=800",
            "specifications": json.dumps({
                "display": "11-inch Dynamic AMOLED 2X",
                "processor": "Snapdragon 8 Gen 2",
                "storage": "128GB (expandable)",
                "camera": "13MP rear, 12MP front",
                "battery": "8400mAh",
                "connectivity": "Wi-Fi 6E, 5G optional",
                "accessories": "S Pen included",
                "operating_system": "Android 13"
            }),
            "features": json.dumps([
                "S pen included",
                "water resistant",
                "dex mode",
                "multi-window",
                "fast charging",
                "samsung knox security"
            ])
        },
        
        # Smart Home
        {
            "name": "Amazon Echo Dot (5th Gen)",
            "description": "Compact smart speaker with Alexa. Controls smart home, plays music, and answers questions with improved sound.",
            "price": 49.99,
            "category": "Smart Home",
            "brand": "Amazon",
            "model": "Echo Dot 5th Gen",
            "image_url": "https://images.unsplash.com/photo-1543512214-318c7553f230?w=800",
            "specifications": json.dumps({
                "speaker": "1.73-inch driver",
                "connectivity": "Wi-Fi, Bluetooth",
                "voice_assistant": "Alexa built-in",
                "smart_home": "Zigbee hub built-in",
                "audio": "3.5mm aux output",
                "power": "15W adapter",
                "dimensions": "3.9 x 3.9 x 3.5 inches",
                "colors": "Charcoal, Glacier White, Deep Sea Blue"
            }),
            "features": json.dumps([
                "alexa voice control",
                "smart home hub",
                "improved sound",
                "drop in calling",
                "music streaming",
                "compact design"
            ])
        },
        
        {
            "name": "Google Nest Hub (2nd Gen)",
            "description": "Smart display with Google Assistant. Perfect for smart home control, video calls, and entertainment.",
            "price": 99.99,
            "category": "Smart Home",
            "brand": "Google",
            "model": "Nest Hub 2nd Gen",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
            "specifications": json.dumps({
                "display": "7-inch touchscreen",
                "resolution": "1024 x 600",
                "connectivity": "Wi-Fi, Bluetooth",
                "voice_assistant": "Google Assistant",
                "smart_home": "Thread border router",
                "audio": "Full-range speaker",
                "camera": "No camera for privacy",
                "sensors": "Ambient EQS, Soli sleep sensing"
            }),
            "features": json.dumps([
                "smart display",
                "google assistant",
                "sleep sensing",
                "video streaming",
                "smart home control",
                "privacy focused"
            ])
        },
        
        # Cameras
        {
            "name": "Canon EOS R10 Mirrorless Camera",
            "description": "Versatile mirrorless camera with 24.2MP sensor and 4K video. Perfect for content creators and photography enthusiasts.",
            "price": 899.99,
            "category": "Camera",
            "brand": "Canon",
            "model": "EOS R10",
            "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=800",
            "specifications": json.dumps({
                "sensor": "24.2MP APS-C CMOS",
                "video": "4K UHD at 30fps",
                "autofocus": "Dual Pixel CMOS AF II",
                "iso_range": "100-32000 (expandable to 51200)",
                "burst_rate": "15 fps electronic shutter",
                "viewfinder": "2.36M-dot OLED EVF",
                "lcd": "3.0-inch vari-angle touchscreen",
                "connectivity": "Wi-Fi, Bluetooth, USB-C"
            }),
            "features": json.dumps([
                "mirrorless design",
                "4K video recording",
                "content creator friendly",
                "dual pixel autofocus",
                "compact and lightweight",
                "RF lens mount"
            ])
        },
        
        {
            "name": "GoPro HERO12 Black",
            "description": "Ultimate action camera with 5.3K video recording and advanced stabilization. Built for adventure and extreme conditions.",
            "price": 399.99,
            "category": "Camera",
            "brand": "GoPro",
            "model": "HERO12 Black",
            "image_url": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800",
            "specifications": json.dumps({
                "video": "5.3K60 / 4K120 / 2.7K240",
                "photo": "27MP photos",
                "stabilization": "HyperSmooth 6.0",
                "waterproof": "33ft (10m) without housing",
                "battery": "Enduro battery included",
                "connectivity": "Wi-Fi 6, Bluetooth",
                "storage": "microSD up to 1TB",
                "voice_control": "Voice commands in 10 languages"
            }),
            "features": json.dumps([
                "5.3K video",
                "waterproof design",
                "hypersmooth stabilization",
                "voice control",
                "rugged construction",
                "live streaming"
            ])
        },
        
        # Fitness & Wearables
        {
            "name": "Apple Watch Series 9 GPS",
            "description": "Advanced smartwatch with health monitoring, fitness tracking, and seamless iPhone integration. Your health companion.",
            "price": 399.99,
            "category": "Wearable",
            "brand": "Apple",
            "model": "Watch Series 9 GPS 45mm",
            "image_url": "https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=800",
            "specifications": json.dumps({
                "display": "45mm Always-On Retina LTPO OLED",
                "processor": "S9 SiP with Neural Engine",
                "health_sensors": "Blood oxygen, ECG, heart rate",
                "fitness": "Workout detection, GPS tracking",
                "battery": "18 hours all-day battery",
                "connectivity": "Wi-Fi, Bluetooth 5.3",
                "water_resistance": "50 meters",
                "operating_system": "watchOS 10"
            }),
            "features": json.dumps([
                "health monitoring",
                "fitness tracking",
                "always-on display",
                "double tap gesture",
                "crash detection",
                "emergency SOS"
            ])
        },
          {
            "name": "Fitbit Charge 6",
            "description": "Advanced fitness tracker with built-in GPS, heart rate monitoring, and Google apps integration. Track your health 24/7.",
            "price": 159.99,
            "category": "Wearable",
            "brand": "Fitbit",
            "model": "Charge 6",
            "image_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800",
            "specifications": json.dumps({
                "display": "1.04-inch color AMOLED",
                "battery": "7+ days battery life",
                "health_sensors": "Heart rate, SpO2, stress management",
                "fitness": "Built-in GPS, 40+ exercise modes",
                "connectivity": "Bluetooth, Wi-Fi",
                "water_resistance": "50 meters",
                "compatibility": "Android and iOS",
                "google_integration": "Google Maps, Google Wallet, YouTube Music"
            }),
            "features": json.dumps([
                "built-in GPS",
                "7-day battery",
                "stress management",
                "google apps",
                "sleep tracking",
                "fitbit premium included"
            ])
        },

        # ADDITIONAL PRODUCTS - PROJECTORS
        {
            "name": "EPSON Home Cinema 2150",
            "description": "Wireless 1080p 3LCD projector with 2500 lumens brightness for home theater and gaming",
            "price": 699.99,
            "category": "Display",
            "subcategory": "projector",
            "style": "home theater",
            "color": "white",
            "rating": 4.6,
            "stock_quantity": 8,
            "brand": "EPSON",
            "model": "Home Cinema 2150",
            "image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800",
            "specifications": json.dumps({
                "resolution": "1920x1080 Full HD",
                "brightness": "2500 lumens",
                "contrast_ratio": "60,000:1",
                "lamp_life": "Up to 7,500 hours",
                "connectivity": "HDMI, USB, Wireless",
                "throw_distance": "8.2 - 24.6 feet",
                "weight": "7.3 lbs",
                "technology": "3LCD"
            }),
            "features": json.dumps([
                "wireless streaming",
                "bright display",
                "full HD quality",
                "home theater optimized",
                "gaming compatible",
                "easy setup"
            ])
        },

        # ELECTRIC SCOOTERS
        {
            "name": "Xiaomi Mi Electric Scooter Pro 2",
            "description": "Premium electric scooter with 45km range, app connectivity, and regenerative braking",
            "price": 449.99,
            "category": "Transportation",
            "subcategory": "electric scooter",
            "style": "urban mobility",
            "color": "black",
            "rating": 4.5,
            "stock_quantity": 12,
            "brand": "Xiaomi",
            "model": "Mi Electric Scooter Pro 2",
            "image_url": "https://images.unsplash.com/photo-1558618047-3e4c7c4aaa03?w=800",
            "specifications": json.dumps({
                "max_speed": "25 km/h",
                "range": "45 km",
                "motor_power": "300W",
                "battery": "12.8Ah lithium battery",
                "charging_time": "8-9 hours",
                "max_load": "100 kg",
                "weight": "14.2 kg",
                "tire_size": "8.5 inch pneumatic"
            }),
            "features": json.dumps([
                "long range",
                "app connectivity",
                "regenerative braking",
                "foldable design",
                "LED display",
                "cruise control"
            ])
        },

        # WIRELESS CHARGERS
        {
            "name": "Anker PowerWave 15 Stand",
            "description": "Fast wireless charging stand with optimized charging for iPhone and Samsung devices",
            "price": 49.99,
            "category": "Accessories",
            "subcategory": "wireless charger",
            "style": "desktop",
            "color": "black",
            "rating": 4.7,
            "stock_quantity": 25,
            "brand": "Anker",
            "model": "PowerWave 15 Stand",
            "image_url": "https://images.unsplash.com/photo-1609592869154-2c0a5ba810e9?w=800",
            "specifications": json.dumps({
                "output_power": "15W max",
                "compatibility": "iPhone 12-15, Samsung Galaxy S series",
                "charging_modes": "5W, 7.5W, 10W, 15W",
                "safety_features": "Temperature control, surge protection",
                "design": "Adjustable stand",
                "cable": "4ft micro USB cable included",
                "indicators": "LED charging status"
            }),
            "features": json.dumps([
                "fast charging",
                "universal compatibility",
                "stand design",
                "safety certified",
                "case friendly",
                "budget friendly"
            ])
        },

        # STREAMING DEVICES
        {
            "name": "NVIDIA Shield TV Pro",
            "description": "4K HDR streaming device powered by Tegra X1+ with Dolby Vision and AI upscaling",
            "price": 199.99,
            "category": "Entertainment",
            "subcategory": "streaming device",
            "style": "premium",
            "color": "black",
            "rating": 4.8,
            "stock_quantity": 18,
            "brand": "NVIDIA",
            "model": "Shield TV Pro",
            "image_url": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800",
            "specifications": json.dumps({
                "processor": "Tegra X1+ processor",
                "storage": "16GB internal + microSD slot",
                "ram": "3GB RAM",
                "video_output": "4K HDR60, Dolby Vision",
                "audio": "Dolby Atmos pass-through",
                "connectivity": "Wi-Fi 5, Gigabit Ethernet, Bluetooth 5.0",
                "usb_ports": "2x USB 3.0",
                "remote": "Voice remote with backlit buttons"
            }),
            "features": json.dumps([
                "4K HDR streaming",
                "AI upscaling",
                "gaming capable",
                "voice control",
                "plex media server",
                "high performance"
            ])
        },

        # POWER BANKS
        {
            "name": "Anker PowerCore III Elite 25600",
            "description": "High-capacity power bank with 87W USB-C PD for laptops, tablets, and phones",
            "price": 129.99,
            "category": "Accessories",
            "subcategory": "power bank",
            "style": "high capacity",
            "color": "black",
            "rating": 4.6,
            "stock_quantity": 20,
            "brand": "Anker",
            "model": "PowerCore III Elite 25600",
            "image_url": "https://images.unsplash.com/photo-1609592866746-1d21ac334d98?w=800",
            "specifications": json.dumps({
                "capacity": "25,600mAh / 94.4Wh",
                "output_power": "87W USB-C PD",
                "ports": "2x USB-C, 1x USB-A",
                "input": "60W USB-C recharging",
                "recharge_time": "2.5 hours with 60W charger",
                "weight": "1.3 lbs",
                "safety": "MultiProtect safety system",
                "compatibility": "MacBook, iPad, iPhone, Samsung, etc."
            }),
            "features": json.dumps([
                "high capacity",
                "laptop charging",
                "fast recharging",
                "multiple ports",
                "travel friendly",
                "premium build"
            ])
        },

        # ROBOT VACUUMS
        {
            "name": "iRobot Roomba j7+",
            "description": "Smart robot vacuum with object avoidance, self-emptying base, and app control",
            "price": 599.99,
            "category": "Smart Home",
            "subcategory": "robot vacuum",
            "style": "premium",
            "color": "charcoal",
            "rating": 4.4,
            "stock_quantity": 10,
            "brand": "iRobot",
            "model": "Roomba j7+",
            "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
            "specifications": json.dumps({
                "suction_power": "10x power-lifting suction",
                "navigation": "PrecisionVision Navigation",
                "battery": "75+ minutes runtime",
                "dustbin": "Self-emptying Clean Base",
                "mapping": "Imprint Smart Mapping",
                "connectivity": "Wi-Fi, app control, voice commands",
                "sensors": "Cliff detect, dirt detect",
                "brush_system": "Dual rubber brushes"
            }),
            "features": json.dumps([
                "object avoidance",
                "self-emptying",
                "smart mapping",
                "pet friendly",
                "app control",
                "voice commands"
            ])
        },

        # BLUETOOTH SPEAKERS (BUDGET)
        {
            "name": "JBL Clip 4",
            "description": "Ultra-portable waterproof speaker with carabiner clip and bold JBL Pro sound",
            "price": 59.99,
            "category": "Audio",
            "subcategory": "portable speaker",
            "style": "ultra-portable",
            "color": "blue",
            "rating": 4.5,
            "stock_quantity": 30,
            "brand": "JBL",
            "model": "Clip 4",
            "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",
            "specifications": json.dumps({
                "driver": "40mm dynamic driver",
                "frequency_response": "120Hz - 20kHz",
                "battery_life": "10 hours",
                "charging_time": "3 hours via USB-C",
                "waterproof": "IP67 rated",
                "bluetooth": "Bluetooth 5.1",
                "weight": "239g",
                "dimensions": "86.2 x 46.2 x 135.8mm"
            }),
            "features": json.dumps([
                "ultra-portable",
                "waterproof",
                "carabiner clip",
                "budget friendly",
                "long battery",
                "outdoor friendly"
            ])
        },

        # COMPUTER MONITORS
        {
            "name": "Dell UltraSharp U2723QE",
            "description": "27-inch 4K USB-C hub monitor with 100% sRGB color accuracy for professionals",
            "price": 569.99,
            "category": "Computer",
            "subcategory": "monitor",
            "style": "professional",
            "color": "black",
            "rating": 4.7,
            "stock_quantity": 15,
            "brand": "Dell",
            "model": "UltraSharp U2723QE",
            "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800",
            "specifications": json.dumps({
                "screen_size": "27 inches",
                "resolution": "3840 x 2160 4K UHD",
                "panel_type": "IPS Black technology",
                "color_gamut": "100% sRGB, 98% DCI-P3",
                "brightness": "400 nits",
                "contrast_ratio": "2000:1",
                "response_time": "5ms (gray to gray)",
                "refresh_rate": "60Hz",
                "connectivity": "USB-C 90W, HDMI, DisplayPort"
            }),
            "features": json.dumps([
                "4K resolution",
                "color accurate",
                "USB-C hub",
                "professional grade",
                "adjustable stand",
                "energy efficient"
            ])
        },

        # MECHANICAL KEYBOARDS
        {
            "name": "Logitech MX Keys S",
            "description": "Advanced wireless keyboard with smart illumination and multi-device connectivity",
            "price": 109.99,
            "category": "Computer",
            "subcategory": "keyboard",
            "style": "wireless",
            "color": "graphite",
            "rating": 4.6,
            "stock_quantity": 22,
            "brand": "Logitech",
            "model": "MX Keys S",
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800",
            "specifications": json.dumps({
                "key_type": "Low-profile scissor switches",
                "layout": "Full-size with number pad",
                "connectivity": "Bluetooth, USB receiver",
                "battery": "10 days (backlit), 5 months (no backlight)",
                "charging": "USB-C",
                "compatibility": "Windows, Mac, Linux, iOS, Android",
                "special_features": "Smart illumination, Logi Options+",
                "dimensions": "430.2 x 131.6 x 20.5mm"
            }),
            "features": json.dumps([
                "wireless connectivity",
                "smart illumination",
                "multi-device",
                "long battery life",
                "professional typing",
                "cross-platform"
            ])
        },

        # AIR PURIFIERS
        {
            "name": "Dyson Pure Cool TP07",
            "description": "Smart air purifier and tower fan with HEPA H13 filtration and app control",
            "price": 549.99,
            "category": "Smart Home",
            "subcategory": "air purifier",
            "style": "tower fan",
            "color": "white-silver",
            "rating": 4.5,
            "stock_quantity": 8,
            "brand": "Dyson",
            "model": "Pure Cool TP07",
            "image_url": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5e?w=800",
            "specifications": json.dumps({
                "filtration": "HEPA H13 + Activated Carbon",
                "room_coverage": "Up to 800 sq ft",
                "air_multiplier": "350° oscillation",
                "sensors": "Particle, Gas, Humidity, Temperature",
                "connectivity": "Wi-Fi, Dyson Link app",
                "controls": "Remote, app, voice (Alexa, Google)",
                "noise_level": "As quiet as 24dB",
                "dimensions": "41.3 x 8.7 x 8.7 inches"
            }),
            "features": json.dumps([                "HEPA filtration",
                "tower fan design",
                "smart sensors",
                "app control",
                "voice commands",
                "premium quality"
            ])
        }
    ]
    
    return budget_products
