class Validation:

    def validate(self,  inputs) -> bool:
        for input in inputs:
            if input == None or len(input) == 0:
                return False
        
        return True