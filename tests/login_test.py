def test_upload_csvfile(client):
    res = client.get("/login")
    assert res.status_code == 200

