import {
    EuiAvatar,
} from '@elastic/eui';
import { getAvatarName } from 'utils/format';


export default function UserAvatar({
    user,
    size = "l",
    initialLength = 1,
    type = "user",
    color = null
}) {
    return (
        <EuiAvatar
            size={size}
            name={getAvatarName(user)}
            imageUrl={user?.profile?.image}
            initialsLength={initialLength}
            type={type}
            // color={color}
        />
    )
}