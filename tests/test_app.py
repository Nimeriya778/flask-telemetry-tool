from tlm_app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_main_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"LTU Telemetry Tool" in response.data
    assert b"Upload a file" in response.data
    assert b"View LTU table" in response.data


def test_upload(client):
    assert client.get("/upload").status_code == 200
    client.post("/upload")


def test_table(client):
    response = client.get("/table?channel=LTU1.1&set=brd")
    assert response.status_code == 200


def test_plot(client):
    response = client.get("/plot/ltu1_1_brd.png")
    assert response.status_code == 200
