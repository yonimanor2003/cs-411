import logging
import requests

from meal_max.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


def get_random() -> float:
    """
    Makes a GET request to random.org to fetche a single random decimal number with two decimal places.
    
    Returns:
        float: A random decimal number between 0 and 1, with two decimal places.

    Raises:
        RuntimeError: If the request times out or fails for other reasons.
        ValueError: If the response from random.org cannot be parsed as a float.
    """
    
    url = "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new"

    try:
        # Log the request to random.org
        logger.info("Fetching random number from %s", url)

        response = requests.get(url, timeout=5)

        # Check if the request was successful
        response.raise_for_status()

        random_number_str = response.text.strip()

        try:
            random_number = float(random_number_str)
        except ValueError:
            raise ValueError("Invalid response from random.org: %s" % random_number_str)

        logger.info("Received random number: %.3f", random_number)
        return random_number

    except requests.exceptions.Timeout:
        logger.error("Request to random.org timed out.")
        raise RuntimeError("Request to random.org timed out.")

    except requests.exceptions.RequestException as e:
        logger.error("Request to random.org failed: %s", e)
        raise RuntimeError("Request to random.org failed: %s" % e)