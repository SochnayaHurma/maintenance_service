

export const errorFieldToMessageMapping = {
    email: "Please enter a valid email.",
    username: "Please enter a username consisting of only letters, numbers, underscores, and dashes.",
    password: "Please choose a password with at least 7 characters."
}

export const parseErrorDetail = (errorDetail) => {
    let errorMessage = "Something went wrong. Contact support.";

    if (Array.isArray(errorDetail?.loc)) {
        if (errorDetail.loc[0] === "path") return errorMessage;
        if (errorDetail.loc[0] === "query") return errorMessage;
        if (errorDetail.loc[0] === "body") {
            const invalidField = errorDetail.loc[2];

            if (errorFieldToMessageMapping[invalidField]) {
                errorMessage = errorFieldToMessageMapping[invalidField];
            } else if (errorDetail?.msg) {
                errorMessage = errorDetail.msg;
            }
        }
    }
    return errorMessage
}

export const extractErrorMessages = (error) => {
    const errorList = [];
    if (typeof error === "string") errorList.push(error);
    if (typeof error?.detail === "string") errorList.push(error.detail);

    if (Array.isArray(error?.detail)) {
        error.detail.forEach((errorDetail) => {
            const errorMessage = parseErrorDetail(errorDetail);
            errorList.push(errorMessage);
        })
    }
    return errorList;
}