from typing import List
from uuid import UUID

import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


async def test_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("147ad7a1-d42a-41fd-8f30-242417429c49"))

    assert (
        err.value.message
        == "Product not find with value: 147ad7a1-d42a-41fd-8f30-242417429c49"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = "9.500"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("147ad7a1-d42a-41fd-8f30-242417429c49"))
    assert (
        err.value.message
        == "Product not find with value: 147ad7a1-d42a-41fd-8f30-242417429c49"
    )
