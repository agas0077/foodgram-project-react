# Standard Library
import io

# Third Party Library
from django.http import HttpResponse
import pandas as pd
from recipes.models import (
    AMOUNT_NAME,
    INGREDIENT_NAME_NAME,
    MEASUREMENT_UNIT_NAME,
)


def create_excel_order_list(queryset_values_list) -> HttpResponse:
    """
    Функция для создания excel-файла списка покупок.
    Возвращает готовый HttpResponse.
    """

    # Создаем датафрейм и переименовываем столбцы
    df = pd.DataFrame(queryset_values_list)
    columns = [INGREDIENT_NAME_NAME, AMOUNT_NAME, MEASUREMENT_UNIT_NAME]
    df.columns = columns

    # Создаем сводную таблицу, чтобы сумировать объем необходимых
    # ингредиентов
    df = df.pivot_table(
        values=AMOUNT_NAME,
        index=[INGREDIENT_NAME_NAME, MEASUREMENT_UNIT_NAME],
        aggfunc=sum,
    ).reset_index()
    df = df[columns]

    # Отправляем файл
    file_name = "Ingredients.xlsx"

    with io.BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            df.to_excel(writer, index=False)

        response = HttpResponse(
            b.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
        )
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response
