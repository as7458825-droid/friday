import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import main1
    ui_class = getattr(main1, "NovaOrb", None) or getattr(main1, "AnimeAssistant", None)
    if ui_class:
        app = ui_class()
        app.run()
    else:
        main1.main()
