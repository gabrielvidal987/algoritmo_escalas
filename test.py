def aste():
    schedule = 'a'
    def tes():
        nonlocal schedule 
        schedule = 'b'
        pass
    tes()
    print(schedule)
    
aste()