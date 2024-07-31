
export const capitalize = (str) => {
    return str ? str[0].toUpperCase() + str.slice(1) : str
}

export const getAvatarName = (user) => {
    return capitalize(user?.profile?.full_name) || capitalize(user?.username) || "Anonymous";
}

const currencyFormatter = new Intl.NumberFormat("en-EU", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
})

export const formatPrice = (price) => (price ? currencyFormatter.format(price) : price);

export const truncate = (str, n = 200, useWordBoundary = false) => {
    if (!str || str?.length <= n) return str;
    const subString = str.substring(0, n - 1);
    return (useWordBoundary ? subString.substring(0, subString.lastIndexOf(" ")) : subString) + "&hellip;";
}