import pytest
from sqlalchemy import insert, select

from src.auth.models import RoleOrm
from conftest import client, async_session_maker


@pytest.fixture(autouse=True, scope='session')
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(RoleOrm).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(RoleOrm).where(RoleOrm.id == 1)
        result = await session.execute(query)
        for result in result.scalars():
            assert f"{result.id, result.name, result.permissions}" == "(1, 'admin', None)", "Role is not added"


def test_register():
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 0,
        "username": "string",
        "role_id": 0
    }
                )

    assert response.status_code == 201, "User is not registered"
