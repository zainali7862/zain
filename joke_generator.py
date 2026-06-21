import requests
import json
from typing import Dict, Optional, List
from enum import Enum

class JokeType(Enum):
    """Different joke API sources and types"""
    OFFICIAL_JOKE_API = "official"
    JOKES_API = "jokes"
    CHUCK_NORRIS = "chuck_norris"
    DAD_JOKES = "dad_jokes"

class JokeGenerator:
    """Generate random jokes from multiple external APIs"""
    
    # API endpoints
    OFFICIAL_JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"
    JOKES_API_URL = "https://v2.jokeapi.dev/joke/Any"
    CHUCK_NORRIS_API_URL = "https://api.chucknorris.io/jokes/random"
    DAD_JOKES_API_URL = "https://icanhazdadjoke.com/"
    
    def __init__(self, timeout: int = 5):
        """
        Initialize the joke generator
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
    
    def get_official_joke(self) -> Optional[Dict]:
        """
        Get a random joke from Official Joke API
        
        Returns:
            Dictionary with joke data or None if failed
        """
        try:
            response = self.session.get(
                self.OFFICIAL_JOKE_API_URL,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "type": "Official Joke API",
                "setup": data.get("setup", ""),
                "punchline": data.get("punchline", ""),
                "full_joke": f"{data.get('setup', '')} {data.get('punchline', '')}",
                "id": data.get("id"),
                "status": "success"
            }
        except requests.RequestException as e:
            print(f"Error fetching from Official Joke API: {e}")
            return None
    
    def get_jokes_api_joke(self, joke_type: str = "Any") -> Optional[Dict]:
        """
        Get a random joke from JokesAPI
        
        Args:
            joke_type: Type of joke (Any, Miscellaneous, Programming, Knock-knock)
        
        Returns:
            Dictionary with joke data or None if failed
        """
        try:
            response = self.session.get(
                self.JOKES_API_URL.replace("Any", joke_type),
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("type") == "twopart":
                joke_text = f"{data.get('setup')} {data.get('delivery')}"
            else:
                joke_text = data.get("joke", "")
            
            return {
                "type": "JokesAPI",
                "category": data.get("category", ""),
                "joke": joke_text,
                "full_joke": joke_text,
                "status": "success"
            }
        except requests.RequestException as e:
            print(f"Error fetching from JokesAPI: {e}")
            return None
    
    def get_chuck_norris_joke(self) -> Optional[Dict]:
        """
        Get a random Chuck Norris joke
        
        Returns:
            Dictionary with joke data or None if failed
        """
        try:
            response = self.session.get(
                self.CHUCK_NORRIS_API_URL,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "type": "Chuck Norris Jokes",
                "joke": data.get("value", ""),
                "full_joke": data.get("value", ""),
                "url": data.get("url", ""),
                "status": "success"
            }
        except requests.RequestException as e:
            print(f"Error fetching from Chuck Norris API: {e}")
            return None
    
    def get_dad_joke(self) -> Optional[Dict]:
        """
        Get a random dad joke
        
        Returns:
            Dictionary with joke data or None if failed
        """
        try:
            response = self.session.get(
                self.DAD_JOKES_API_URL,
                headers={"Accept": "application/json"},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "type": "Dad Jokes",
                "joke": data.get("joke", ""),
                "full_joke": data.get("joke", ""),
                "id": data.get("joke_sid", ""),
                "status": "success"
            }
        except requests.RequestException as e:
            print(f"Error fetching from Dad Jokes API: {e}")
            return None
    
    def get_random_joke(self, api_type: JokeType = None) -> Dict:
        """
        Get a random joke from a random or specified API
        
        Args:
            api_type: Specific API to use, or None for random selection
        
        Returns:
            Dictionary with joke data
        """
        import random
        
        if api_type is None:
            api_type = random.choice(list(JokeType))
        
        if api_type == JokeType.OFFICIAL_JOKE_API:
            return self.get_official_joke() or self._get_fallback_joke()
        elif api_type == JokeType.JOKES_API:
            return self.get_jokes_api_joke() or self._get_fallback_joke()
        elif api_type == JokeType.CHUCK_NORRIS:
            return self.get_chuck_norris_joke() or self._get_fallback_joke()
        elif api_type == JokeType.DAD_JOKES:
            return self.get_dad_joke() or self._get_fallback_joke()
    
    def _get_fallback_joke(self) -> Dict:
        """Get a fallback joke in case APIs fail"""
        fallback_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What did the ocean say to the beach? Nothing, it just waved!",
            "Why don't eggs tell jokes? They'd crack each other up!",
        ]
        import random
        return {
            "type": "Fallback Joke",
            "joke": random.choice(fallback_jokes),
            "full_joke": random.choice(fallback_jokes),
            "status": "fallback"
        }
    
    def get_multiple_jokes(self, count: int = 5) -> List[Dict]:
        """
        Get multiple random jokes
        
        Args:
            count: Number of jokes to retrieve
        
        Returns:
            List of joke dictionaries
        """
        jokes = []
        for _ in range(count):
            joke = self.get_random_joke()
            if joke:
                jokes.append(joke)
        return jokes
    
    def print_joke(self, joke: Dict) -> None:
        """
        Pretty print a joke
        
        Args:
            joke: Joke dictionary
        """
        print("\n" + "="*60)
        print(f"📝 Source: {joke.get('type', 'Unknown')}")
        
        if "setup" in joke and "punchline" in joke:
            print(f"Setup: {joke['setup']}")
            print(f"Punchline: {joke['punchline']}")
        elif "joke" in joke:
            print(f"Joke: {joke['joke']}")
        elif "full_joke" in joke:
            print(f"Joke: {joke['full_joke']}")
        
        print(f"Status: {joke.get('status', 'unknown')}")
        print("="*60 + "\n")
    
    def close(self) -> None:
        """Close the session"""
        self.session.close()

def main():
    """Main function to demonstrate the joke generator"""
    print("🎭 Welcome to the Random Joke Generator! 🎭\n")
    
    generator = JokeGenerator()
    
    try:
        # Get a random joke from any API
        print("Getting a random joke from a random API...\n")
        joke = generator.get_random_joke()
        generator.print_joke(joke)
        
        # Get jokes from specific APIs
        print("\n" + "="*60)
        print("Getting jokes from each API source:")
        print("="*60 + "\n")
        
        # Official Joke API
        print("1️⃣ Official Joke API:")
        official_joke = generator.get_official_joke()
        if official_joke:
            generator.print_joke(official_joke)
        
        # JokesAPI
        print("2️⃣ JokesAPI:")
        jokes_api_joke = generator.get_jokes_api_joke()
        if jokes_api_joke:
            generator.print_joke(jokes_api_joke)
        
        # Chuck Norris API
        print("3️⃣ Chuck Norris Jokes:")
        chuck_joke = generator.get_chuck_norris_joke()
        if chuck_joke:
            generator.print_joke(chuck_joke)
        
        # Dad Jokes API
        print("4️⃣ Dad Jokes:")
        dad_joke = generator.get_dad_joke()
        if dad_joke:
            generator.print_joke(dad_joke)
        
        # Get multiple jokes
        print("\n" + "="*60)
        print("Getting 3 random jokes:")
        print("="*60)
        multiple_jokes = generator.get_multiple_jokes(3)
        for i, joke in enumerate(multiple_jokes, 1):
            print(f"\nJoke {i}:")
            generator.print_joke(joke)
    
    finally:
        generator.close()

if __name__ == "__main__":
    main()
