import controllers as ctrl

ctrl.welcome()
while True:
    try:
        if ctrl.main():
            ctrl.main()
    except KeyboardInterrupt:
        print("See Youu~")
        break
