import uuid

def test_auth_flow(client):

    # 1-  sign up new user

    username = f"test_{uuid.uuid4().hex[:8]}"
    password = "123456"

    sign_up_resp = client.put(
        "/token",
        json={
            "username": username,
            "password": password,
            "surName": "pyTest_module",
            "name": "pyTest_module",
            "patronymicName": "pyTest_module",
            "jobTitle": "pyTest_module",
            "userRole": "pyTest_module",
        },
    )

    assert sign_up_resp.status_code == 200
    data = sign_up_resp.json()
    assert data["status"] == "ok"
    assert data["data"]["username"] == username
    access_1 = data["data"]["accessToken"]
    refresh_1 = data["data"]["refreshToken"]
    user_id = data["data"]["id"]

    # 2 - sign in with each data

    sign_in_resp = client.post(
        "/token",
        json={
            "username": username,
            "password": password,
        },
    )

    assert sign_in_resp.status_code == 200
    data_login = sign_in_resp.json()
    assert data_login["status"] == "ok"
    assert data_login["data"]["username"] == username
    access_2 = data_login["data"]["accessToken"]
    refresh_2 = data_login["data"]["refreshToken"]

    # CHECH: tokens should be another after sign in
    assert access_2 != access_1
    assert refresh_2 != refresh_1

    # 3 - get current user by access-token

    me_resp = client.get(
        "/user",
        headers={"Authorization": f"Bearer {access_2}"},
    )

    assert me_resp.status_code == 200
    data_me = me_resp.json()
    assert data_me["status"] == "ok"
    assert data_me["data"]["id"] == user_id
    assert data_me["data"]["username"] == username

    # 4 - update user tokens by refresh-token

    refresh_resp = client.post(
        "/token/refresh",
        json={"refresh": refresh_2},
    )

    assert refresh_resp.status_code == 200
    data_refresh = refresh_resp.json()
    assert data_refresh["status"] == "ok"
    assert data_refresh["data"]["username"] == username

    access_3 = data_refresh["data"]["accessToken"]
    refresh_3 = data_refresh["data"]["refreshToken"]

    # new pair accessToken|refreshToken must be another when elders
    
    assert access_3 != access_2
    assert refresh_3 != refresh_2

    # 5 - CHECK get user by NEW access-token 

    me_resp2 = client.get(
        "/user",
        headers={"Authorization": f"Bearer {access_3}"},
    )

    assert me_resp2.status_code == 200
    data_me2 = me_resp2.json()
    assert data_me2["status"] == "ok"
    assert data_me2["data"]["id"] == user_id
    assert data_me2["data"]["username"] == username
