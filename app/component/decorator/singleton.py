import threading

def singleton():
    """
    Defines a function called singleton, which is a decorator (a special function that modifies a class to make it a singelton).
    :return Wrapper:
    """
    class Wrapper:
        """
        Creates a helper class called Wrapper, which will handle the singleton logic.
        """
        _instances = {} # Creates a storage room (dictionary) to keep track of instances of different class, if a class is already stored here, we return the same instance instead of making a new one.
        _locks = {} # Creates a storage for locks. Each class gets its own lock to prevent two threads or more from creating the same instance at the same time.

        def __init__(self, cls):
            """
            This runs when the wrapper is created. It takes a class (cls) and prepares it to be a singleton.
            """
            self.other_class = cls # Stores the class that will become a singleton so we can create or return its instance later.
            if cls not in self._locks: # If the class doesn't have a lock yet, create one.
                self._locks[cls] = threading.RLock() # This lock will prevent multiple threads from creating multiple instances.


        def __call__(self, *args, **kwargs):
            """
            This runs when we try to create an instance of the decorated class. the __call__ method allows the class 'Wrapper' to behave like a function.
            :param args:
            :param kwargs:
            :return:
            """
            if self.other_class not in self._instances: # Checks if we already have an instance of this class. If yes return the existing one. If no, create the new one.
                with self._locks[self.other_class]: # Locks the class so only one thread can create an instance at a time. Prevents multiple copies.
                    if self.other_class not in self._instances: # Double-checks if the instance exists. This prevents two threads or more creating instances.
                        self._instances[self.other_class] = self.other_class(*args, **kwargs) # Creates the instance and stores it in '_instances', so next time, we return this instead of making a new one.
            return self._instances[self.other_class] # Returns the stored instance of the class. If an instance already exists, it gives you the same one.

    Wrapper.is_singelton = True # Adds a marker (is_singleton = true) to indicate that the class was wrapped with the singleton decorator. This isn't necessary but could be useful for debugging or validation.

    return Wrapper # Returns the Wrapper class, which will replace the original class with the singleton logic.
