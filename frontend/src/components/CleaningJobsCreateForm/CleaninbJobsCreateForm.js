import React from "react";
import {
    EuiButton,
    EuiFieldNumber,
    EuiFieldText,
    EuiForm,
    EuiFormRow,
    EuiSpacer,
    EuiSuperSelect,
    EuiTextArea
} from "@elastic/eui";


export default function CleaningJobsCreateForm (props) {
    const {
        form,
        handleSubmit,
        getFormErrors,
        localErrors,
        onInputChange,
        onCleaningTypeChange,
        isLoading,
        cleaningTypeOptions,
    } = props;
    return (
        <React.Fragment>
            <EuiForm
                component="form"
                onSubmit={handleSubmit}
                isInvalid={Boolean(getFormErrors().length)}
                error={getFormErrors()}
            >
                <EuiFormRow
                    label="Название услуги:"
                    helpText="Что вы хотели бы чтоб уборщики видели в первую очередь?"
                    isInvalid={Boolean(localErrors.name)}
                    error={"Пожалуйста введите корректное название."}
                >
                    <EuiFieldText
                        name="name"
                        value={form.name}
                        onChange={(e) => onInputChange(e.target.name, e.target.value)}
                    />
                </EuiFormRow>
                <EuiFormRow
                    label="Выберите тип уборки"
                >
                    <EuiSuperSelect
                        options={cleaningTypeOptions}
                        valueOfSelected={form.cleaning_type}
                        onChange={(value) => onCleaningTypeChange(value)}
                        itemLayoutAlign="top"
                        hasDividers
                    />
                </EuiFormRow>
                <EuiFormRow
                    label="Оплата в час: "
                    helpText="Укажите разумную цену за час выполнения данной работы."
                    isInvalid={Boolean(localErrors.price)}
                    error={"Цена должна соответствовать формату: 9.99"}
                >
                    <EuiFieldNumber
                        name="price"
                        icon="currency"
                        placeholder="19.99"
                        value={form.price}
                        onChange={(e) => onInputChange(e.target.name, e.target.value)}
                    />
                </EuiFormRow>
                <EuiFormRow
                    label="Описание услуги"
                    helpText="Что вы хотите, чтобы потенциальные уборщики знали о ньюансах данной услуги."
                    isInvalid={Boolean(localErrors.description)}
                    error={"Пожалуйста введите корректное значение."}
                >
                    <EuiTextArea
                        name="description"
                        placeholder="Я считаю что..."
                        value={form.description}
                        onChange={(e) => onInputChange(e.target.name, e.target.value)}
                    />
                </EuiFormRow>
                <EuiSpacer />
                <EuiButton type="submit" isLoading={isLoading} fill>
                    Создать услугу
                </EuiButton>
            </EuiForm>
        </React.Fragment>
    )
}