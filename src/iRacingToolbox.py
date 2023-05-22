import click


@click.command()
@click.option('--session-id', help='Session number of the race', required=True)
def compute_results(session_id):
    click.secho(f"Yep it's empty but your id is {session_id}")


if __name__ == '__main__':
    compute_results()


# TODO Rewrite the client to use httpx instead of requests for the api calls
# TODO Make an inventory of all use cases
# TODO Reimplement use cases using pandas
# TODO Move to poetry for the management of dependencies
