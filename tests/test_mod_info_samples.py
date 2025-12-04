"""
Test version extraction from real mod_info.json samples.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.installer import ModInstaller


# Sample mod_info.json files from real Starsector mods
MOD_INFO_SAMPLES = {
    "Roider Union": r"""{
    "id": "roider",
    "name": "Roider Union",
    "author": "SafariJohn",
    "utility": "false",
    "version": { "major":"2", "minor": "2", "patch": "6" },
    "description": "Adds the Roider Union, an alliance of independent asteroid miners and minor corporations.",
    "gameVersion": "0.98a-RC8",
    "jars":["jars/RoiderUnion.jar"],
    "modPlugin":"roiderUnion.ModPlugin",
    "dependencies": [
        {
            "id": "lw_lazylib",
            "name": "LazyLib"
        },
        {
            "id": "MagicLib",
            "name": "MagicLib"
        },
        {
            "id": "RetroLib",
            "name": "RetroLib"
        }
    ]
}""",

    "Random-Assortment-of-Things": r"""{
  "id": "assortment_of_things",
  "name": "Random Assortment of Things",
  "author": "Lukas04 & SnazzyPantsMcGee",
  "utility": "false",
  "version": "3.2.4",
  "description": "A collection of things I create whenever a random idea pops up into my head.",
  "gameVersion": "0.98a-RC8",
  "jars": ["jars/RandomAssortmentofThings.jar"],
  "modPlugin": "assortment_of_things.RATModPlugin",
  "dependencies": [
    {
      "id": "lunalib",
      "name": "LunaLib"
    },
    {
      "id": "MagicLib",
      "name": "MagicLib"
    },
	{
      "id": "shaderLib",
      "name": "GraphicsLib"
    },
	#{
    #  "id": "nexerelin",
    #  "name": "Nexerelin"
    #},
  ]
}
""",

    "LunaLib": r"""{
  "id": "lunalib",
  "name": "LunaLib",
  "author": "Lukas04",
  "utility": "false",
  "version": "2.0.4",
  "description": "Library including utilities for players and mod developers.",
  "gameVersion": "0.98a-RC5",
  "jars": [
    "jars/LunaLib.jar",
    #"jars/LunaLib-Kotlin.jar",
    "jars/libs/fuzzywuzzy-1.3.0.jar"
  ],
  "modPlugin": "lunalib.LunaLibPlugin",
  "dependencies": [
    {
      "id": "lw_lazylib",
      "name": "LazyLib"
    }
  ]
}
""",

    "Nexerelin": r"""{
    "id":"nexerelin",
    "name":"Nexerelin",
    "author":"Histidine (original by Zaphide)",
    "version":{
        "major":0,
        "minor":12, 
        "patch":"1b"
    },
    "description":"Join a faction and conquer the Sector!",
    "gameVersion":"0.98a-RC8",
    "totalConversion":false,
    "jars":["jars/ExerelinCore.jar"],
    "dependencies": [
        {"id": "lw_lazylib", "name": "LazyLib"},
        {"id": "MagicLib", "name": "MagicLib"},
    ],
    "modPlugin":"exerelin.plugins.ExerelinModPlugin",
}""",

    "MarketRetrofits-master": r"""{
	"id":"aaamarketRetrofits", # internal id
	"name":"market retrofits", # displayed to the player
	"author":"Alricdragon",
	"version":"0.2.5",
	"description":"libary for changeing stats of markets",
	"gameVersion":"0.98a-RC5",
	"jars":["jars/marketRetrofit.jar"],
	"modPlugin":"data.scripts.marketReplacer_startup",
}
""",

    "Grand.Colonies2.1.b": r"""{
    "id": "GrandColonies",
    "name": "Grand.Colonies",
    "author": "SirHartley & Lukas04",
    "version": "2.1.b",
    "description": "Adds infinite additional building slots to a colony.",
    "gameVersion": "0.98a",
    "jars":["jars/GrandColonies.jar"],
    "modPlugin":"grandcolonies.plugins.ModPlugin",
    "dependencies": [
        {
            "id": "lw_lazylib",
            "name": "LazyLib",
        },
        {
            "id": "lunalib",
            "name": "LunaLib",
        },
    ]
}
""",

    "GraphicsLib": r"""{
    "id": "shaderLib",
    "name": "zz GraphicsLib",
    "author": "DarkRevenant",
    "version": "1.12.1",
    "utility": "true",
    "description": "An arcane tome of black magic and sorcery.",
    "gameVersion": "0.98a-RC8",
    "jars":["jars/Graphics.jar"],
    "modPlugin":"org.dark.shaders.ShaderModPlugin",
    "dependencies": [
        {
            "id": "lw_lazylib",
            "name": "LazyLib",
            "version": "3.0.0"
        },
    ],
}
""",

    "MagicLib": r"""{
  "id": "MagicLib",
  "name": "MagicLib",
  "author": "Modding Community: Dark.Revenant, LazyWizard, Nicke, Originem, Rubi, Schaf-Unschaf, Snrasha, Tartiflette, Wisp, Wyvern...",
  "utility": "false",
  # Using the long version format lets the game correctly compare major/minor/patch versions.
  "version": { "major": '1', "minor": '5', "patch": '6' },
  "description": "A collection of classes to aid modding. Not a mod in itself, but required by other mods.",
  "gameVersion": "0.98a-RC7",
  "dependencies": [
    {
      "id": "lw_lazylib",
      "name": "LazyLib"
      # "version": "3.0.0" # Remove the specific version for future-proofing.
    }
  ],
  "jars": [ "jars/MagicLib.jar", "jars/MagicLib-Kotlin.jar" ],
  "modPlugin": "org.magiclib.Magic_modPlugin"
}
""",

    "Meme Portraits": r"""{
	"id":"memeportraits", # internal id
	"name":"Meme portraits", # displayed to the player
	"author":"mitrone",
	"version":"1.06",
	"description":"Resolves the issue of Starsector being too immersive and non-shitpostworthy by adding some completely unrelated characters.",
	"gameVersion":"0.95a-RC15",
}
""",
}


def test_version_extraction_from_samples():
    """Test that we can extract versions from all real mod_info.json samples."""
    installer = ModInstaller(lambda msg, **kwargs: print(msg))
    
    print("\n" + "="*80)
    print("Testing Version Extraction from Real mod_info.json Samples")
    print("="*80)
    
    total = len(MOD_INFO_SAMPLES)
    successful = 0
    failed = []
    
    for mod_name, json_content in MOD_INFO_SAMPLES.items():
        version = installer._extract_version_from_text(json_content)
        mod_id = installer._extract_id_from_text(json_content)
        
        if version != 'unknown':
            successful += 1
            status = "✓"
            print(f"\n{status} {mod_name}")
            print(f"  ID: {mod_id or 'N/A'}")
            print(f"  Version: {version}")
        else:
            failed.append(mod_name)
            status = "✗"
            print(f"\n{status} {mod_name}")
            print(f"  ID: {mod_id or 'N/A'}")
            print(f"  Version: FAILED TO EXTRACT")
            print(f"  Content preview: {json_content[:200]}...")
    
    print("\n" + "="*80)
    print(f"Results: {successful}/{total} successful")
    
    if failed:
        print(f"Failed: {', '.join(failed)}")
    
    print("="*80 + "\n")
    
    # Assert all succeeded
    assert successful == total, f"Failed to extract version from: {failed}"


if __name__ == "__main__":
    test_version_extraction_from_samples()
